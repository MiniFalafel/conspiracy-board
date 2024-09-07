
class Log:
    # ONLY static methods

    log_level = 0 # 0 = NONE, 1 = error, 2 = err + warn, 3 = warn + info, 4 = info + trace???

    @staticmethod
    def __log(tag, message, lvl):
        # Check the log level
        if Log.log_level >= lvl:
            print("[%s]: %s" % (tag, message))

    @staticmethod
    def error(message):
        Log.__log("ERROR", message, 1)
        breakpoint()

    @staticmethod
    def warn(message):
        Log.__log("WARN", message, 2)

    @staticmethod
    def info(message):
        Log.__log("INFO", message, 3)

    @staticmethod
    def trace(message):
        Log.__log("TRACE", message, 4)