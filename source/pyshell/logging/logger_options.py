class LoggerOptions:
    """
    Defines options used to configure logger instances.
    """
    def __init__(self,
        print_cmd: bool = True,
        print_cwd: bool = True,
        print_backend: bool = True,
        print_exit_code: bool = True,
        print_timestamps: bool = True,
        print_duration: bool = True,
        add_newline_after_header: bool = True,
        add_newline_before_footer: bool = True,
        add_newline_after_footer: bool = True,
        cmd_header_banner_char: str = ">",
        cmd_header_banner_width: int = 40,
        cmd_footer_banner_char: str = "<",
        cmd_footer_banner_width: int = 40,
        cmd_header_banner_prefix: str = "[PyShell] ",
        cmd_footer_banner_prefix: str = "[PyShell] "):
        """
        Initializes the object.
        @param print_cmd Whether to print the command invocation.
        @param print_cwd Whether to print the current working directory for the
          command.
        @param print_backend Whether to print the backend used to execute the
          command.
        @param print_exit_code Whether to print the exit code of the command.
        @param print_timestamps Whether to print the start and end timestamp
          for the command.
        @param print_duration Whether to print the command execution duration.
        @param add_newline_after_header Whether to add a newline after the
          command header.
        @param add_newline_before_footer Whether to add a newline before the
          command footer.
        @param add_newline_after_footer Whether to add a newline after the
          command footer.
        @param cmd_header_banner_char The character to use for the command
          header banner.
        @param cmd_header_banner_width The width of the command header banner.
        @param cmd_footer_banner_char The character to use for the command
          footer banner.
        @param cmd_footer_banner_width The width of the command footer banner.
        @param cmd_header_banner_prefix The prefix to use for each line in the
          command header banner.
        @param cmd_footer_banner_prefix The prefix to use for each line in the
          command footer banner.
        """
        self._print_cmd = print_cmd
        self._print_cwd = print_cwd
        self._print_backend = print_backend
        self._print_exit_code = print_exit_code
        self._print_timestamps = print_timestamps
        self._print_duration = print_duration
        self._add_newline_after_header = add_newline_after_header
        self._add_newline_before_footer = add_newline_before_footer
        self._add_newline_after_footer = add_newline_after_footer
        self._cmd_header_banner_char = cmd_header_banner_char
        self._cmd_header_banner_width = cmd_header_banner_width
        self._cmd_footer_banner_char = cmd_footer_banner_char
        self._cmd_footer_banner_width = cmd_footer_banner_width
        self._cmd_header_banner_prefix = cmd_header_banner_prefix
        self._cmd_footer_banner_prefix = cmd_footer_banner_prefix

    @property
    def print_cmd(self) -> bool:
        """
        Whether to print the command invocation.
        """
        return self._print_cmd


    @property
    def print_cwd(self) -> bool:
        """
        Whether to print the current working directory for the command.
        """
        return self._print_cwd


    @property
    def print_backend(self) -> bool:
        """
        Whether to print the backend used to execute the command.
        """
        return self._print_backend


    @property
    def print_exit_code(self) -> bool:
        """
        Whether to print the exit code of the command.
        """
        return self._print_exit_code


    @property
    def print_timestamps(self) -> bool:
        """
        Whether to print the start and end timestamp for the command.
        """
        return self._print_timestamps


    @property
    def print_duration(self) -> bool:
        """
        Whether to print the command execution duration.
        """
        return self._print_duration


    @property
    def add_newline_after_header(self) -> bool:
        """
        Whether to add a newline after the command header.
        """
        return self._add_newline_after_header


    @property
    def add_newline_before_footer(self) -> bool:
        """
        Whether to add a newline before the command footer.
        """
        return self._add_newline_before_footer


    @property
    def add_newline_after_footer(self) -> bool:
        """
        Whether to add a newline after the command footer.
        """
        return self._add_newline_after_footer


    @property
    def cmd_header_banner_char(self) -> str:
        """
        The character to use for the command header banner.
        """
        return self._cmd_header_banner_char


    @property
    def cmd_header_banner_width(self) -> int:
        """
        The width of the command header banner.
        """
        return self._cmd_header_banner_width


    @property
    def cmd_footer_banner_char(self) -> str:
        """
        The character to use for the command footer banner.
        """
        return self._cmd_footer_banner_char


    @property
    def cmd_footer_banner_width(self) -> int:
        """
        The width of the command footer banner.
        """
        return self._cmd_footer_banner_width


    @property
    def cmd_header_banner(self) -> str:
        """
        The string to use for the command header banner.
        """
        return self.cmd_header_banner_char * self.cmd_header_banner_width


    @property
    def cmd_footer_banner(self) -> str:
        """
        The string to use for the command footer banner.
        """
        return self.cmd_footer_banner_char * self.cmd_footer_banner_width


    @property
    def cmd_header_banner_prefix(self) -> str:
        """
        The prefix to use for each line in the command header banner.
        """
        return self._cmd_header_banner_prefix


    @property
    def cmd_footer_banner_prefix(self) -> str:
        """
        The prefix to use for each line in the command footer banner.
        """
        return self._cmd_footer_banner_prefix
