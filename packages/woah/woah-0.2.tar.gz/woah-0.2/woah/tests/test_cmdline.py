import subprocess
import sys
import unittest
from unittest import mock

from woah import cmdline


class CmdlineTest(unittest.TestCase):
    @mock.patch("woah.cmdline.sys.stderr.write")
    def test_msg_funcs(self, mock_sys_stderr):
        cmdline.backoff_msg("msg1", True)
        cmdline.backoff_msg("msg2", False)

        cmdline.pass_msg("msg3", True)
        cmdline.pass_msg("msg4", False)

        mock_sys_stderr.assert_has_calls(
            [
                mock.call("msg1"),
                mock.call("\n"),
                mock.call("msg2"),
                mock.call("\n"),
                mock.call("msg4"),
                mock.call("\n"),
            ]
        )

    @mock.patch("woah.cmdline.pass_msg")
    @mock.patch("woah.cmdline.backoff_msg")
    @mock.patch("woah.cmdline.time.sleep")
    @mock.patch("woah.cmdline.cpu_count", return_value=4)
    @mock.patch("woah.cmdline.os.getloadavg", return_value=(1.0, 1.0, 1.0))
    @mock.patch("woah.cmdline.os.execv")
    @mock.patch("woah.cmdline.shutil.which", return_value="/bin/echo")
    def test_passes_immediately(
        self,
        mock_shutil_which,
        mock_execv,
        mock_getloadavg,
        mock_cpu_count,
        mock_time_sleep,
        mock_backoff_msg,
        mock_pass_msg,
    ):

        cmdline.main(["echo", "hi there"])

        mock_execv.assert_called_with("/bin/echo", ["echo", "hi there"])

        mock_time_sleep.assert_not_called()
        mock_shutil_which.assert_called_with("echo")
        mock_backoff_msg.assert_not_called()
        mock_pass_msg.assert_called_with("1.00 < 4.80, passed", True)

    @mock.patch("woah.cmdline.pass_msg")
    @mock.patch("woah.cmdline.backoff_msg")
    @mock.patch("woah.cmdline.time.sleep")
    @mock.patch("woah.cmdline.cpu_count", return_value=4)
    @mock.patch(
        "woah.cmdline.os.getloadavg",
        side_effect=[(123.0, None, None), (123.0, None, None), (1.0, None, None)],
    )
    @mock.patch("woah.cmdline.os.execv")
    @mock.patch("woah.cmdline.shutil.which", return_value="/bin/echo")
    def test_passes_after_a_few(
        self,
        mock_shutil_which,
        mock_execv,
        mock_getloadavg,
        mock_cpu_count,
        mock_time_sleep,
        mock_backoff_msg,
        mock_pass_msg,
    ):
        t = 0.0

        def sleep(delta):
            nonlocal t
            t += delta

        mock_time_sleep.side_effect = sleep

        cmdline.main(["echo", "hi there"])

        mock_execv.assert_called_with("/bin/echo", ["echo", "hi there"])

        self.assertEqual(1.0 + 1.61, t)
        mock_shutil_which.assert_called_with("echo")
        mock_backoff_msg.assert_has_calls(
            [
                mock.call("123.00 >= 4.80, waiting 1.00s", True),
                mock.call("123.00 >= 4.80, waiting 1.61s", False),
            ]
        )
        mock_pass_msg.assert_called_with("1.00 < 4.80, passed", False)

    @mock.patch("woah.cmdline.sys.argv")
    @mock.patch("woah.cmdline.sys.exit")
    @mock.patch("woah.cmdline.time.sleep")
    @mock.patch("woah.cmdline.cpu_count", return_value=4)
    @mock.patch("woah.cmdline.os.getloadavg", return_value=(1.0, 1.0, 1.0))
    @mock.patch("woah.cmdline.os.execv")
    @mock.patch("woah.cmdline.shutil.which", return_value="/bin/echo")
    def test_default_sys_argv(
        self,
        mock_shutil_which,
        mock_execv,
        mock_getloadavg,
        mock_cpu_count,
        mock_time_sleep,
        mock_exit,
        mock_argv,
    ):
        cmdline.sys.argv = ["woah", "echo", "hi there"]
        cmdline.main()
        mock_execv.assert_called_with("/bin/echo", ["echo", "hi there"])

    @mock.patch("woah.cmdline.sys.stderr.write")
    @mock.patch("woah.cmdline.time.sleep")
    @mock.patch("woah.cmdline.cpu_count", return_value=4)
    @mock.patch("woah.cmdline.os.getloadavg", return_value=(1.0, 1.0, 1.0))
    @mock.patch("woah.cmdline.os.execv")
    @mock.patch("woah.cmdline.shutil.which", return_value=None)
    def test_error_messages(
        self,
        mock_shutil_which,
        mock_execv,
        mock_getloadavg,
        mock_cpu_count,
        mock_time_sleep,
        mock_stderr_write,
    ):

        with self.assertRaises(SystemExit):
            cmdline.main([])

        with self.assertRaises(SystemExit):
            cmdline.main(["echo", "hi"])

    def test_exec(self):
        output = subprocess.check_output(
            [sys.executable, "woah/cmdline.py", "echo", "hi   there"], encoding="utf-8"
        )
        self.assertEqual("hi   there\n", output)
