from campy.private.backend_base import ConsoleBackendBase

class InteractiveConsoleBackend(ConsoleBackendBase):
    def clear_console(self):
        pass

    def set_console_font(self, font):
        pass

    def set_console_size(self, console_size):
        pass

    def get_console_line(self):
        return input()

    def put_console(self, line, stderr=False):
        print(line)

    # def echo_console(self):
    #     pass

    # def end_line_console(self):
    #     pass
