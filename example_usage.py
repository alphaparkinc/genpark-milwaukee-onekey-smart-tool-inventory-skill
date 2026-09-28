from client import MilwaukeeOneKeySmartToolSkill
import json

def test():
    skill = MilwaukeeOneKeySmartToolSkill()
    print("=== Testing Milwaukee Tool ONE-KEY Smart Hardware Skill ===")
    
    bench = skill.run_benchmark_smart_tools()
    print(json.dumps(bench, indent=2))

if __name__ == "__main__":
    test()
