import engine

def execute_plan(plan: dict) -> list:
    logs = []
    
    # Display the AI's blazing-fast reasoning on the frontend UI
    if "thought_process" in plan:
        logs.append({
            "step": {"action": "REASONING"}, 
            "status": "success", 
            "detail": plan["thought_process"]
        })

    for step in plan.get("steps", []):
        action = step.get("action")
        try:
            if action == "navigate":
                msg = engine.navigate(step.get("url"))
            elif action == "search_web":
                msg = engine.search_web(step.get("query"))
            elif action == "type":
                msg = engine.type_text(step.get("text"))
            elif action == "press_key":
                msg = engine.press_key(step.get("key"))
            elif action == "desktop_mode":
                msg = engine.desktop_mode()
            elif action == "open_app":
                msg = engine.open_app(step.get("app_name"))
            elif action == "run_command":
                msg = engine.run_ps_command(step.get("command"))
            elif action == "system_reply":
                msg = step.get("message")
            elif action == "wait":
                msg = engine.wait(step.get("seconds", 2))
            elif action == "force_close":
                msg = engine.force_close(step.get("app_exe"))
            else:
                msg = f"Unknown core action: {action}"
            
            logs.append({"step": step, "status": "success" if "Unknown" not in msg else "error", "detail": msg})
        except Exception as e:
            logs.append({"step": step, "status": "error", "detail": str(e)})
            
    return logs