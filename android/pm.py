# Implementation of native Android "pm list packages"
# command in MicroPython.
import ffi
import jni

# Bootstrap JVM
jni.cls("java/lang/Object")
rt = ffi.open("/system/lib/libandroid_runtime.so")
# Note in 5.x, function may be called: jint registerFrameworkNatives(JNIEnv* env)
# https://android-review.googlesource.com/#/c/157981/1/core/jni/AndroidRuntime.cpp
registerNatives = rt.func("p", "Java_LoadClass_registerNatives", "pp")
registerNatives(jni.env(), None)

# This is older, Java-level way to register framework natives, but
# "registerNatives" method may be absent in 4.x devices, and class
# itself is removed in 5.x.
#fw = jni.cls("com.android.internal.util.WithFramework")
#fw.registerNatives()

ServiceManager = jni.cls("android/os/ServiceManager")
pm = ServiceManager.getService("package")
#print("Service:", pm)
IPackageManager = jni.cls("android/content/pm/IPackageManager")
#print("IPackageManager", IPackageManager)
IPackageManager_Stub = jni.cls("android/content/pm/IPackageManager$Stub")
#print(IPackageManager_Stub)
mPm = IPackageManager_Stub.asInterface(pm)
#print("mPm:", mPm, mPm.toString())
#print("=================")
res = mPm.getInstalledPackages(0, 0)
#res = pm.getInstalledPackages(0)
#print("=================")
#print(res)
ls = res.getList()
#print("***", ls)
#print(ls.toString())
for p in ls:
    print("package:" + p.packageName)
