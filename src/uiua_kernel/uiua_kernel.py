import subprocess
from ipykernel.kernelbase import Kernel
import os
from ansi2html import Ansi2HTMLConverter

ansi_to_html = Ansi2HTMLConverter(dark_bg=True)

class UIUAKernel(Kernel):
    implementation = 'Uiua'
    implementation_version = '1.0'
    language = 'uiua'
    language_version = '0.1'
    language_info = {
        'name': 'uiua',
        'mimetype': 'text/plain',
        'file_extension': 'ua',
    }
    banner = "Uiua Kernel"

    def do_execute(
        self,
        code,
        silent,
        store_history=True,
        user_expressions=None,
        allow_stdin=False,
        *,
        cell_id=None,
    ):
        if not silent:
            # self.send_response(
            #     self.iopub_socket,
            #     'stream',
            #     {
            #         'name': 'comment',
            #         'text': f"We will try run\n```\nuiua.exe eval {code}\n```"
            #     }
            # )
            env = os.environ.copy()
            env["CLICOLOR_FORCE"] = "True"
            proc = subprocess.Popen(
                args     = ["uiua.exe", "eval", code.encode("utf-8")],
                #stdin    = subprocess.PIPE,
                stdout   = subprocess.PIPE,
                stderr   = subprocess.PIPE,
                encoding ="utf-8",
                #text   = True,
                #universal_newlines=True,
                env = env,
            )
            stdout, stderr = proc.communicate(code)
            if proc.returncode == 0:
                self.send_response(
                    self.iopub_socket,
                    'execute_result',
                    {
                        'execution_count': 1,
                        'data': {
                            "text/html":ansi_to_html.convert(stdout),

                        },
                        'metadata': {},
                    }
                )
            else:
                self.send_response(
                    self.iopub_socket,
                    'stream',
                    {
                        'name': 'stderr',
                        'text': stderr,
                    }
                )
                self.send_response(self.iopub_socket,
                    'execute_result',
                    {
                        'execution_count': 1,
                        'data': {
                            "text/html":ansi_to_html.convert(stdout),
                        },
                        'metadata': {},
                    }
                )
        return {
            'status'           : 'ok',
            'execution_count'  : self.execution_count,
            'payload'          : [],
            'user_expressions' : {}
        }
    
    async def do_debug_request(self, msg):
        raise NotImplementedError

    def do_apply(self, content, bufs, msg_id, reply_metadata):
        """DEPRECATED"""
        raise NotImplementedError
    def do_clear(self):
        """DEPRECATED since 4.0.3"""
        raise NotImplementedError

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=UIUAKernel)
