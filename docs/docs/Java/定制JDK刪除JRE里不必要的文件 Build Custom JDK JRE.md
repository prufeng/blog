Build Custom JDK/JRE
====
```
#!/bin/sh
# Remove all not-needed files, see http://www.oracle.com/technetwork/java/javase/jre-8-readme-2095710.html
# Documentation
rm -f jre/README.txt
rm -f jre/THIRDPARTYLICENSEREADME.txt
rm -f jre/THIRDPARTYLICENSEREADME-JAVAFX.txt
rm -f jre/Welcome.html
# optional files 
rm -f jre/lib/ext/jfxrt.jar
rm -f jre/lib/ext/access-bridge.jar
rm -f jre/lib/ext/access-bridge-32.jar
rm -f jre/lib/ext/nashorn.jar
rm -f jre/bin/rmid.*
rm -f jre/bin/rmiregistry.*
rm -f jre/bin/tnameserv.*
rm -f jre/bin/keytool.*
rm -f jre/bin/kinit.*
rm -f jre/bin/klist.*
rm -f jre/bin/ktab.*
rm -f jre/bin/policytool.*
rm -f jre/bin/orbd.*
rm -f jre/bin/servertool.*
rm -f jre/bin/javaws.*
rm -f jre/lib/jfr.*
# can be deleted when private application runtime is used (like launch4j)
# rm -f jre/bin/java.exe
# launch4j uses javaw.exe. So do NOT delete!
rm -f jre/bin/javacpl.exe
rm -f jre/bin/jabswitch.exe
rm -f jre/bin/java_crw_demo.dll
rm -f jre/bin/JavaAccessBridge-32.dll
rm -f jre/bin/JavaAccessBridge.dll
rm -f jre/bin/JAWTAccessBridge-32.dll
rm -f jre/bin/JAWTAccessBridge.dll
rm -f jre/bin/WindowsAccessBridge-32.dll
rm -f jre/bin/WindowsAccessBridge.dll
rm -f jre/bin/wsdetect.dll
rm -f jre/bin/deploy.dll
rm -f jre/bin/javacpl.cpl
rm -f jre/lib/deploy.jar
rm -f jre/lib/plugin.jar
rm -Rf /s /q jre/bin/dtplugin
rm -Rf /s /q jre/bin/plugin2
rm -Rf /s /q jre/lib/deploy
# JavaFX related
rm -f jre/lib/javafx.properties
rm -f jre/lib/jfxswt.jar
rm -f jre/bin/jfx*
rm -f jre/bin/decora_sse.dll
rm -f jre/bin/fxplugins.dll
rm -f jre/bin/glass.dll
rm -f jre/bin/glib-lite.dll
rm -f jre/bin/gstreamer-lite.dll
rm -f jre/bin/javafx_font.dll
```
