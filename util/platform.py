
class Platform()
    # Constant: UNKNOWN
    # Indicates that the type of system cannot be determined.
    UNKNOWN = 0

    # Constant: MAC
    # Indicates that the system is some variety of Apple Macintosh.
    MAC = 1

    # Constant: UNIX
    # Indicates that the system is some variety of Unix or Linux.
    UNIX = 2

    # Constant: WINDOWS
    # Indicates that the system is some variety of Microsoft Windows.
    WINDOWS = 3

    @staticmethod
    def get_platform():
        if (platform != -1) return platform;
        String name = System.getProperty("os.name", "").toLowerCase();
        if (name.startsWith("mac")) return platform = MAC;
        if (name.startsWith("windows")) return platform = WINDOWS;
        if (name.startsWith("microsoft")) return platform = WINDOWS;
        if (name.startsWith("ms")) return platform = WINDOWS;
        if (name.startsWith("unix")) return platform = UNIX;
        if (name.startsWith("linux")) return platform = UNIX;
        return platform = UNKNOWN;

    @staticmethod
    def is_mac():
        return get_platform() == MAC

    @staticmethod
    def is_unix():
        return get_platform() == UNIX

    @staticmethod
    def is_windows():
        return get_platform() == MAC

    """

/* Static method: setFileTypeAndCreator(filename, type, creator) */
/**
 * Sets the Macintosh file type and creator.  This method is ignored on non-Mac
 * platforms.
 *
 * @usage Platform.setFileTypeAndCreator(filename, type, creator);
 * @param filename The name of the file
 * @param type A four-character string indicating the file type
 * @param creator A four-character string indicating the file type
 */
    public static void setFileTypeAndCreator(String filename, String type, String creator) {
        if (!isMac()) return;
        try {
            setFileTypeAndCreator(new File(filename), type, creator);
        } catch (Exception ex) {
            /* Empty */
        }
    }

/* Static method: setFileTypeAndCreator(file, type, creator) */
/**
 * Sets the Macintosh file type and creator.  This method is ignored on non-Mac
 * platforms.
 *
 * @usage Platform.setFileTypeAndCreator(file, type, creator);
 * @param file The <code>File</code> object corresponding to the file
 * @param type A four-character string indicating the file type
 * @param creator A four-character string indicating the file type
 */
    public static void setFileTypeAndCreator(File file, String type, String creator) {
        if (!isMac()) return;
        try {
            Class<?> mrjOSTypeClass = Class.forName("com.apple.mrj.MRJOSType");
            Class<?> mrjFileUtilsClass = Class.forName("com.apple.mrj.MRJFileUtils");
            Class[] sig1 = { Class.forName("java.lang.String") };
            Constructor<?> constructor = mrjOSTypeClass.getConstructor(sig1);
            Class[] sig2 = { Class.forName("java.io.File"), mrjOSTypeClass, mrjOSTypeClass };
            Method setFileTypeAndCreator = mrjFileUtilsClass.getMethod("setFileTypeAndCreator", sig2);
            Object[] args1 = { (type + "    ").substring(0, 4) };
            Object osType = constructor.newInstance(args1);
            Object[] args2 = { (creator + "    ").substring(0, 4) };
            Object creatorType = constructor.newInstance(args2);
            Object[] args3 = { file, osType, creatorType };
            setFileTypeAndCreator.invoke(null, args3);
        } catch (Exception ex) {
            /* Empty */
        }
    }

/* Static method: copyFileTypeAndCreator(newFile, oldFile) */
/**
 * Sets the Macintosh file type and creator for the new file using the old file
 * as a model.  This method is ignored on non-Mac platforms.
 *
 * @usage Platform.copyFileTypeAndCreator(oldFile, newFile);
 * @param oldFile The <code>File</code> object corresponding to the existing file
 * @param newFile The <code>File</code> object corresponding to the new file
 */
    public static void copyFileTypeAndCreator(File oldFile, File newFile) {
        if (!isMac()) return;
        try {
            Class<?> mrjOSTypeClass = Class.forName("com.apple.mrj.MRJOSType");
            Class<?> mrjFileUtilsClass = Class.forName("com.apple.mrj.MRJFileUtils");
            Class[] sig1 = { Class.forName("java.io.File") };
            Method getFileType = mrjFileUtilsClass.getMethod("getFileType", sig1);
            Method getFileCreator = mrjFileUtilsClass.getMethod("getFileCreator", sig1);
            Class[] sig2 = { Class.forName("java.io.File"), mrjOSTypeClass, mrjOSTypeClass };
            Method setFileTypeAndCreator = mrjFileUtilsClass.getMethod("setFileTypeAndCreator", sig2);
            Object[] args1 = { oldFile };
            Object osType = getFileType.invoke(null, args1);
            Object creatorType = getFileCreator.invoke(null, args1);
            Object[] args2 = { newFile, osType, creatorType };
            setFileTypeAndCreator.invoke(null, args2);
        } catch (Exception ex) {
            /* Empty */
        }
    }
    """

