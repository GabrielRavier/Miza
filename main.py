import os, time, datetime, traceback, psutil

python = ("python3", "python")[os.name == "nt"]
try:
    os.system("color")
except:
    print(traceback.format_exc())


def delete(f):
    while f in os.listdir():
        try:
            os.remove(f)
            break
        except:
            print(traceback.format_exc())
        time.sleep(1)

sd = "shutdown.json"
rs = "restart.json"
hb = "heartbeat.json"

delete(sd)
delete(rs)
delete(hb)

while not sd in os.listdir():
    delete(rs)
    delete(hb)
    proc = psutil.Popen([python, "bot.py"], shell=True)
    print("Bot started with PID \033[1;34;40m" + str(proc.pid) + "\033[1;37;40m.")
    time.sleep(8)
    try:
        print("\033[1;32;40mHeartbeat started\033[1;37;40m.")
        alive = True
        while alive:
            f = open(hb, "wb")
            f.close()
            print(
                "\033[1;36;40m Heartbeat at "
                + str(datetime.datetime.now())
                + "\033[1;37;40m."
            )
            for i in range(16):
                time.sleep(0.5)
                ld = os.listdir()
                if rs in ld or sd in ld:
                    alive = False
                    break
            if not alive or hb in os.listdir():
                alive = False
                break
        found = True
        while found:
            found = False
            try:
                for child in proc.children():
                    child.kill()
                    found = True
            except psutil.NoSuchProcess:
                break
        while True:
            try:
                proc.kill()
            except psutil.NoSuchProcess:
                break
        if sd in os.listdir():
            break
        print("\033[1;31;40mBot closed without shutdown signal, restarting...\033[1;37;40m")
    except KeyboardInterrupt:
        raise
    except:
        print(traceback.format_exc())
    time.sleep(0.5)
    
delete(hb)
delete(rs)
delete(sd)
        
print("Shutdown signal confirmed. Press [ENTER] to close.")
input()
