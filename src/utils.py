def interpret_steps(aniodesde, aniohasta):
    steps_ahead = int((aniohasta - aniodesde + 1)*18)
    return {"steps": steps_ahead, "anio_desde": aniodesde}

def interpret_months(i: int):
   return int((i) % 18 + 1)

def interpret_year(anio: int,i: int):
    return int(anio + i // 18)