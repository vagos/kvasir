import tempfile
import subprocess
import os
from kvasir.hooks import hookimpl
from kvasir.program import Property, Language
from kvasir.utils import logger

class SyscallTrace(Property):
    """System calls made by the program when exercised on representative inputs."""

    def to_lm(self):
        return ""

@hookimpl
def apply(program):
    if "inputs" not in program.annotations:
        logger.warning("No inputs found; skipping syscall tracing.")
        return

    inputs = program["inputs"].value
    syscall_set = set()
    
    cmd = make_command(program)
    syscall_set |= trace_syscalls(cmd)

    program["syscall_trace"] = SyscallTrace("syscall_trace", sorted(syscall_set))
    logger.debug(f"Extracted syscalls: {sorted(syscall_set)}")

@hookimpl
def knowledge(kb, program):
    kb.add_logic("can(syscall_trace(p)).", "Program can be traced for syscalls.")
    kb.add_logic(":- do(syscall_trace(p)), not do(inputs(p)).", "Syscalls can only be traced if inputs are available.")
    kb.add_logic(":- do(syscall_trace(p)), pure(p).", "Syscalls should not be traced for pure programs without side effects.")

import platform

def is_macos():
    return platform.system() == "Darwin"

def is_linux():
    return platform.system() == "Linux"

import re

def make_command(program) -> list[str]:
    lang = program.language
    program_path = program.entry.as_posix()
    match lang:
        case Language.JS:
            return ["node", program_path]
        case Language.C | Language.HS:
            return [program_path]
        case _:
            raise ValueError(f"Unsupported language: {lang}")

def extract_syscalls(trace: str) -> set[str]:
    syscall_pattern = re.compile(r"^(\w+)\(")
    return {
        match.group(1)
        for line in trace.splitlines()
        if (match := syscall_pattern.match(line.strip()))
    }

def trace_syscalls(command: list[str]) -> set[str]:
    timeout = 3
    try:
        if is_linux():
            tracer = ["strace", "-f", "-e", "trace=all"]
        elif is_macos():
            raise RuntimeError("Syscall tracing is not supported on macOS.")
        else:
            raise RuntimeError("Unsupported OS for syscall tracing.")

        proc = subprocess.run(
            tracer + command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        trace = proc.stderr.decode()
        logger.debug(f"Syscall trace output:\n{trace}")
        return extract_syscalls(trace)
    except Exception as e:
        logger.warning(f"Syscall tracing failed: {e}")
        return set()
