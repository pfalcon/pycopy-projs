# This demonstrates calling Linux syscalls "directly" (well, using a libc
# proxy, but that appears to be "recommended" method anyway).
import ffilib
import uos


C = ffilib.libc()

# Different Linux archs have different syscall values (not like every one
# is different, but there're a few "patterns", plus potentially any may add
# minor glitches on top of a common pattern).
# Below are the numbers for x86_64, etc., but not for i386!
SYS_write = 1
SYS_getpid = 39

# Different syscalls have different signatures
syscall0 = C.func("l", "syscall", "i")
syscall_write = C.func("l", "syscall", "iiPi")


print("pid:", syscall0(SYS_getpid))

res = syscall_write(SYS_write, 1, "hello\n", 6)
print(res)
if res == -1:
    print("errno:", uos.errno())
