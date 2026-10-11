"""Command dispatcher. Domain modules own policy and behavior."""
import argparse
import json
import sys
from . import __version__
from .storage import Invalid, Run, digest, read_json, write_json
from . import workflow, conformance, manifests, reporting, sandbox, sessions, probes, corpus


def parser():
    p = argparse.ArgumentParser(description="Record evidence, seal behavioral contracts and measure conformance.")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="verb", required=True)
    init = sub.add_parser("init", help="Create a private evidence run")
    init.add_argument("run")
    init.add_argument("--target", required=True)
    init.add_argument("--language", required=True)
    init.add_argument("--source-root", action="append", default=[])
    for verb in ("observe", "probe", "session", "packet", "check", "approve", "approve-cases", "handoff", "validate", "audit", "status", "resume", "report", "incident", "export", "sandbox"):
        cmd = sub.add_parser(verb)
        cmd.add_argument("run")
        if verb in {"observe", "incident", "session"}:
            cmd.add_argument("--record", required=True)
        if verb in {"check", "approve"}:
            cmd.add_argument("--spec", required=True)
        if verb in {"approve", "approve-cases"}:
            cmd.add_argument("--review", required=True)
        if verb == "approve-cases":
            cmd.add_argument("--cases", required=True)
        if verb in {"handoff", "export", "packet"}:
            cmd.add_argument("--dest", required=True)
        if verb == "report":
            cmd.add_argument("--output")
        if verb == "validate":
            cmd.add_argument("--cases", required=True)
            cmd.add_argument("--oracle", required=True, help="JSON array of adapter command arguments")
            cmd.add_argument("--candidate", required=True, help="JSON array of adapter command arguments")
            cmd.add_argument("--timeout", type=float, default=10)
        if verb == "probe":
            cmd.add_argument("--plan", required=True)
            cmd.add_argument("--adapter", required=True, help="JSON array of oracle command arguments")
            cmd.add_argument("--timeout", type=float, default=10)
        if verb == "sandbox":
            cmd.add_argument("command", nargs=argparse.REMAINDER)
    scan = sub.add_parser("scan")
    scan.add_argument("manifest")
    sha = sub.add_parser("digest", help="Hash canonical JSON for a review record")
    sha.add_argument("file")
    cmp = sub.add_parser("compare")
    cmp.add_argument("--left", required=True)
    cmp.add_argument("--right", required=True)
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.verb == "init":
            result = workflow.initialize(args.run, args.target, args.language, args.source_root)
        elif args.verb == "scan":
            result = manifests.scan(args.manifest)
        elif args.verb == "digest":
            result = {"sha256": digest(read_json(args.file)), "encoding": "canonical-json-no-newline"}
        elif args.verb == "compare":
            result = reporting.compare(args.left, args.right)
        else:
            run = Run(args.run)
            with run.lock():
                if args.verb != "incident":
                    run.verify()
                verb = args.verb
                if verb == "observe":
                    result = workflow.observe(run, read_json(args.record))
                elif verb == "probe":
                    if not 0 < args.timeout <= 300:
                        raise Invalid("Adapter timeout must be between 0 and 300 seconds")
                    result = probes.probe(run, read_json(args.plan), json.loads(args.adapter), args.timeout)
                elif verb == "session":
                    result = sessions.register(run, read_json(args.record))
                elif verb == "packet":
                    result = sessions.packet(run, args.dest)
                elif verb == "check":
                    result = workflow.check(run, read_json(args.spec))
                elif verb == "approve":
                    result = workflow.approve(run, read_json(args.spec), read_json(args.review))
                elif verb == "approve-cases":
                    result = corpus.approve(run, read_json(args.cases), read_json(args.review))
                elif verb == "handoff":
                    result = workflow.handoff(run, args.dest)
                elif verb == "incident":
                    result = workflow.incident(run, read_json(args.record))
                elif verb == "validate":
                    if not 0 < args.timeout <= 300:
                        raise Invalid("Adapter timeout must be between 0 and 300 seconds")
                    result = conformance.validate(run, read_json(args.cases), json.loads(args.oracle),
                                                  json.loads(args.candidate), args.timeout)
                elif verb in {"audit", "resume"}:
                    result = run.verify()
                elif verb in {"status", "report"}:
                    result = reporting.report(run)
                    if verb == "report" and args.output:
                        from .paths import output_path
                        write_json(output_path(run, args.output), result)
                elif verb == "export":
                    result = reporting.export(run, args.dest)
                elif verb == "sandbox":
                    cmd = args.command[1:] if args.command[:1] == ["--"] else args.command
                    result = sandbox.launch(run, cmd)
                else:
                    raise Invalid("Unknown command")
        print(json.dumps(result, sort_keys=True, allow_nan=False))
        if result.get("status") in {"rejected", "incomplete-or-divergent"} or result.get("exit_code", 0):
            return 2
        return 0
    except (Invalid, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"error": str(exc), "status": "rejected"}), file=sys.stderr)
        return 2
    except OSError:
        print(json.dumps({"error": "Filesystem or process operation failed; inspect private run integrity", "status": "rejected"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
