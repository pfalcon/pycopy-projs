# Example of communicating with another process over pseudoterminal (pty).
# Try is as e.g.: micropython ptyterm.py micropython
import sys
import os
import termios
import uselect as select
import ffilib

if len(sys.argv) < 2:
    print("Usage: %s <command>..." % sys.argv[0])
    sys.exit(0)


libc = ffilib.libc()

# Linux man page says:
# "getpt() is glibc-specific; use posix_openpt(3) instead."
# But some other libc's have getpt(), but lack posix_openpt(),
# e.g. Android Bionic.
getpt = libc.func("i", "getpt", "")
# grantpt() is not available in every libc, e.g. Android Bionic
# up to some version lacked it.
#grantpt = libc.func("i", "grantpt", "i")
unlockpt = libc.func("i", "unlockpt", "i")
ptsname = libc.func("s", "ptsname", "i")

fd_m = getpt()
#assert grantpt(fd_m) == 0
assert unlockpt(fd_m) == 0
slave_tty = ptsname(fd_m)
print("Connecting using pty:", slave_tty)

pid = os.fork()

if pid:
    term_state = termios.tcgetattr(0)
    termios.setraw(0)

    poll = select.poll()
    poll.register(0, select.POLLIN)
    poll.register(fd_m, select.POLLIN)

    quit = False
    try:
        while not quit:
            res = poll.poll()
            #print(res)
            for fd, event in res:
                if fd == 0:
                    data = os.read(0, 64)
                    os.write(fd_m, data)
                else:
                    if event & select.POLLIN:
                        data = os.read(fd_m, 128)
                        os.write(1, data)
                    if event & select.POLLHUP:
                        quit = True
                        break
    finally:
        termios.tcsetattr(0, 0, term_state)

    os.close(fd_m)
    os.waitpid(pid, 0)

else:
    os.close(fd_m)
    fd_s = os.open(slave_tty, os.O_RDWR)
    os.close(0)
    os.close(1)
    os.close(2)
    os.dup(fd_s)
    os.dup(fd_s)
    os.dup(fd_s)
    os.execvp(sys.argv[1], sys.argv[1:])
