from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager()
    # https://github.com/android/ndk-samples/blob/master/gles3jni/app/src/main/cpp/CMakeLists.txt
    # platform         status
    #   (0 12)           ES2/ES3 not supported
    #   [12, 18)         ES2 only; for ES3, app do dynamic load/detection
    #                    this applies to the situations that:
    #                        - minimum API is set to less than 18. In this case
    #                          there is no ES3 header/lib support inside NDK
    #                        - the built APK might be running on newer API phones
    #                    with dynamic loading of ES3, the same APK would still be able
    #                    to use ES3. Otherwise, app would stuck with ES2 even phone is
    #                    is newer than the minimum API level (for example, Android-27 etc).
    #
    #   [18, 24)         ES2 & ES3
    #                    If app is built to only support API-18 or later,
    #                    set minimum api level to 18 is good enough, NDK supprts ES3
    #                    with the right header and lib files. No need to use ES3 dynamic
    #                    detection.
    #   [24, infinite)   ES2 & ES3 & Vulkan
    builder.add(settings={"arch": "armv7", "os.api_level": "18"})
    builder.add(settings={"arch": "armv8", "os.api_level": "21"})
    builder.add(settings={"arch": "x86", "os.api_level": "18"})
    builder.add(settings={"arch": "x86_64", "os.api_level": "21"})
    builder.run()
