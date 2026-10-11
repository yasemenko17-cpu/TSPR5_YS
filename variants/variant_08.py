def hill_status(scopes: list, week: int, total_weeks: int) -> dict:
    # 1. Перевірка помилок у суворому порядку
    if not scopes:
        raise ValueError("Немає скоупів")
    if not (1 <= week <= total_weeks):
        raise ValueError("Тиждень поза циклом")
        
    for sc in scopes:
        name = sc.get("name")
        history = sc.get("history", [])
        if len(history) < week:
            raise ValueError(f"Скоуп «{name}»: історія коротша за тиждень {week}")
        pos = history[week - 1]
        if not (0 <= pos <= 100):
            raise ValueError(f"Скоуп «{name}»: позиція поза 0-100")
            
    processed_scopes = []
    m_total = 0
    m_done = 0
    
    # 2. Обчислення параметрів для кожного скоупа
    for sc in scopes:
        name = sc["name"]
        must = sc["must"]
        history = sc["history"]
        pos = history[week - 1]
        
        if must:
            m_total += 1
            if pos == 100:
                m_done += 1
                
        # Лінійний прогноз на кінець циклу (цілочисельне ділення)
        projected = min(100, pos * total_weeks // week)
        
        # Визначення фази
        if pos == 100:
            phase = "готово"
        elif pos < 50:
            phase = "вгору"
        else:
            phase = "вниз"
            
        # Визначення статусу
        if pos == 100:
            status = "готово"
        elif projected >= 100:
            status = "встигає"
        elif projected >= 70:
            status = "під ризиком"
        else:
            status = "не встигає"
            
        processed_scopes.append({
            "name": name,
            "phase": phase,
            "position": pos,
            "projected": projected,
            "status": status
        })
        
    must_done_str = f"{m_done} з {m_total}"
    
    # 3. Визначення рішення та фокусу
    focus = []
    if week == total_weeks:
        unfin_must = [s["name"] for s, sc in zip(processed_scopes, scopes) if sc["must"] and s["position"] < 100]
        unfin_opt = [s["name"] for s, sc in zip(processed_scopes, scopes) if not sc["must"] and s["position"] < 100]
        
        if unfin_must:
            decision = "запобіжник спрацював: повернути пітч на шейпінг"
            focus = unfin_must
        elif unfin_opt:
            decision = "випуск за графіком з урізанням обсягу"
            focus = unfin_opt
        else:
            decision = "випуск за графіком"
            focus = []
    else:
        not_succeed_must = [s["name"] for s, sc in zip(processed_scopes, scopes) if sc["must"] and s["status"] == "не встигає"]
        at_risk_must = [s["name"] for s, sc in zip(processed_scopes, scopes) if sc["must"] and s["status"] == "під ризиком"]
        
        if not_succeed_must:
            decision = "урізати обсяг: звільнити час для обов'язкового"
            focus = not_succeed_must
        elif at_risk_must:
            decision = "стежити за обов'язковим"
            focus = at_risk_must
        else:
            decision = "рухаємось за планом"
            focus = []
            
    return {
        "week": week,
        "scopes": processed_scopes,
        "must_done": must_done_str,
        "decision": decision,
        "focus": focus
    }