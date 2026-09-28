import sys, json
from client import MilwaukeeOneKeySmartToolSkill

def handle_mcp():
    skill = MilwaukeeOneKeySmartToolSkill()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(skill.run_benchmark_smart_tools(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-milwaukee-onekey-smart-tool-inventory-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "track_tool_location", "description": "Locate smart power tools via BLE mesh beacon network.", "inputSchema": {"type": "object", "properties": {"tool_serial": {"type": "string"}}}},
                    {"name": "configure_torque_profile", "description": "Program repeatable torque limits and RPM curve.", "inputSchema": {"type": "object", "properties": {"tool_serial": {"type": "string"}, "target_torque_ft_lbs": {"type": "number"}}}},
                    {"name": "enforce_security_lockout", "description": "Lock or unlock stolen tools rendering motors inoperable.", "inputSchema": {"type": "object", "properties": {"tool_serial": {"type": "string"}, "lock": {"type": "boolean"}}}},
                    {"name": "fetch_fleet_telematics", "description": "Audit trigger cycles and battery telemetry across fleet.", "inputSchema": {"type": "object"}},
                    {"name": "run_benchmark_smart_tools", "description": "Run smart hardware integration benchmark.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "track_tool_location":
                    res = skill.track_tool_location(args.get("tool_serial", ""))
                elif tname == "configure_torque_profile":
                    res = skill.configure_torque_profile(args.get("tool_serial", ""), args.get("target_torque_ft_lbs", 450))
                elif tname == "enforce_security_lockout":
                    res = skill.enforce_security_lockout(args.get("tool_serial", ""), args.get("lock", True))
                elif tname == "fetch_fleet_telematics":
                    res = skill.fetch_fleet_telematics()
                else:
                    res = skill.run_benchmark_smart_tools()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
