from app.database import get_db_connection
from app.auth import hash_password

def seed_database():
    """Siembra los datos iniciales para CasaLista si aún no existen."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Usuario de prueba
    existing_user = cursor.execute("SELECT id FROM users WHERE email = 'prueba@casalista.co'").fetchone()
    if not existing_user:
        hashed_pwd = hash_password("casalista123")
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, city)
            VALUES (?, ?, ?, ?)
        """, ("Dylan Gamero", "prueba@casalista.co", hashed_pwd, "Bogotá, D.C."))
        user_id = cursor.lastrowid
    else:
        user_id = existing_user["id"]

    # 2. Las 8 Categorías Oficiales
    categories = [
        ("cat_pintura", "Pintura y acabados", "Paredes, techos y marcos", "format_paint", "Dificultad básica • Est. COP", "info", "facil", "paredes techos marcos rodillo pintura brochas lija", 1),
        ("cat_paredes", "Paredes y pequeños daños", "Resanes, fisuras y huecos", "handyman", "Secado rápido • Bricolaje fácil", "info", "facil", "resanes fisuras huecos masilla yeso espatula grietas", 2),
        ("cat_instalacion", "Instalación y organización", "Repisas, cuadros y cortineros", "shelves", "Requiere brocas y nivel", "caution", "intermedio", "repisas cuadros cortineros taladro anclajes chazos", 3),
        ("cat_electricidad", "Electricidad básica", "Interruptores y plafones", "lightbulb", "Cortar breaker antes", "warning", "precaucion", "electricidad interruptores plafones tomas breakers bombillo", 4),
        ("cat_plomeria", "Plomería menor", "Fugas de sifón, empaques y grifos", "build", "Llave de paso requerida", "caution", "intermedio", "plomeria fugas sifon empaques grifos agua llave goteo teflon", 5),
        ("cat_muebles", "Muebles y puertas", "Ajuste de bisagras y chapas", "door_front", "Destornillador + lubricación", "info", "facil", "muebles puertas bisagras chapas cerradura lubricante madera", 6),
        ("cat_bano_cocina", "Baño y cocina", "Silicona, duchas y rejillas", "shower", "Prevención antihongos", "caution", "intermedio", "bano cocina silicona duchas rejillas sellado humedad calafateo", 7),
        ("cat_mantenimiento", "Mantenimiento preventivo", "Filtros, campanas y techos", "shield", "Inspección periódica", "info", "facil", "mantenimiento preventivo filtros campanas revision humedad", 8)
    ]

    for cat in categories:
        cursor.execute("""
            INSERT OR REPLACE INTO categories (id, name, subtitle, icon, badge_text, badge_type, difficulty_tag, keywords, order_num)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, cat)

    # 3. Catálogo de Tareas Predefinidas
    tasks = [
        # Cat Pintura
        (
            "task_pintar_pared",
            "cat_pintura",
            "Pintar una pared interior",
            "Herramientas básicas • Rodillo y cinta",
            "Aprende a calcular la pintura exacta, preparar la superficie, resanar imperfecciones y aplicar manos uniformes para renovar cualquier habitación.",
            "green",
            "Reparación sencilla",
            "Se realiza sobre piso firme a nivel del suelo sin riesgo de caídas ni exposición a voltajes peligrosos.",
            "Fácil",
            "~3 a 4 h",
            45000,
            "Vinilo Tipo 1 Satinado",
            "~25 m²/gal",
            "2 capas",
            "2 a 4 hrs",
            "~65%",
            "Ventila adecuadamente el espacio y protege rodapiés y tomacorrientes antes de comenzar para evitar manchas indeseadas y reducir tiempo de limpieza.",
            "Pared lisa, sin marcas de rodillo ni sombras de empalme, con bordes perfectamente definidos.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuDkGFETcHQ3pfGR2EJTTRntA0g0QNXshRyMmOPh9zcNomqvrVm6ZiONoetRBO9MofXbkyjGhZqK3nYKueRz_N1Ti6mXCegllLmOYnq-LfIsYJLuTQpdNOqoMtBUaL834t1Dz5aztrRYxVeCq_MPRYsYqCvqQDmNIMQ6RqrmrYVvWrkq0_5m_GHZ4RR94gDmVCtTcm_BIAw5DHEV9JjkFNE84g6OluagACeesPO63mY4jVfMZT_T_rD6",
            0,
            1
        ),
        (
            "task_retocar_zocalos",
            "cat_pintura",
            "Retocar zócalos y molduras",
            "Pintura perimetral • Brocha de recorte",
            "Repara raspones y manchas en zócalos de madera o yeso con brocha fina.",
            "green",
            "Reparación sencilla",
            "Trabajo seguro a ras de suelo.",
            "Fácil",
            "~1 a 2 h",
            25000,
            "Esmalte al agua",
            "~30 m lineales/cuarto",
            "2 capas",
            "1 a 2 hrs",
            "~70%",
            "Usa cinta de enmascarar en el piso para asegurar una línea recta perfecta.",
            "Bordes limpios y zócalos protegidos sin goteos.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBsmIvtuPilapbZVRiuZiLFOlz4J4dvLlD0gfE4QnlMDJ7wEIrNrZBWJ-FsK76I3Ii-L1LG_F-bD3JKHEifrVYmfJInwifGvQZyGvQ1Ti6LpPt5CrbBYAJRdAirxh9iuPu-s_NVoM906ycICln6Sep3eRFy_uGkAQEvJ1BAeQQy3LCwshzwMs_fqHsSYfyvCFiai0hRLkzB7Pw8hKEnxY6bBuSUICBrNa5oHXjlghb3IgH_6nnMSYdp",
            0,
            0
        ),
        # Cat Paredes
        (
            "task_resanar_agujeros",
            "cat_paredes",
            "Tapar huecos de puntilla o chazo",
            "Estuco plástico interior • Espátula",
            "Rellena pequeños orificios dejados por cuadros o clavos en muros de mampostería o drywall.",
            "green",
            "Reparación sencilla",
            "No compromete la estructura del muro y los materiales no son tóxicos.",
            "Muy fácil",
            "~30 a 45 min",
            18000,
            "Estuco plástico",
            "Hasta 25 huecos por tubo",
            "1 a 2 capas",
            "1 hr",
            "~80%",
            "Aplica la masilla en ángulo de 45° y retira el exceso al ras para minimizar el lijado posterior.",
            "Superficie completamente plana y lista para aplicar pintura de retoque.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuDkGFETcHQ3pfGR2EJTTRntA0g0QNXshRyMmOPh9zcNomqvrVm6ZiONoetRBO9MofXbkyjGhZqK3nYKueRz_N1Ti6mXCegllLmOYnq-LfIsYJLuTQpdNOqoMtBUaL834t1Dz5aztrRYxVeCq_MPRYsYqCvqQDmNIMQ6RqrmrYVvWrkq0_5m_GHZ4RR94gDmVCtTcm_BIAw5DHEV9JjkFNE84g6OluagACeesPO63mY4jVfMZT_T_rD6",
            0,
            1
        ),
        (
            "task_reparar_grieta_superficial",
            "cat_paredes",
            "Reparar fisura superficial en estuco",
            "Cinta de malla de fibra • Masilla",
            "Corrige micro-fisuras cosméticas menores a 1mm en muros sin daño estructural.",
            "yellow",
            "Precaución requerida",
            "Requiere verificar que la fisura no atraviese columnas o vigas estructurales.",
            "Moderada",
            "~1 a 2 h",
            32000,
            "Masilla elástica y malla",
            "~5 metros lineales",
            "2 capas",
            "3 hrs",
            "~60%",
            "Si la grieta mide más de 2 mm o se ensancha con el tiempo, consulta a un ingeniero estructural.",
            "Fisura sellada elásticamente que previene reaparición de marcas.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBsmIvtuPilapbZVRiuZiLFOlz4J4dvLlD0gfE4QnlMDJ7wEIrNrZBWJ-FsK76I3Ii-L1LG_F-bD3JKHEifrVYmfJInwifGvQZyGvQ1Ti6LpPt5CrbBYAJRdAirxh9iuPu-s_NVoM906ycICln6Sep3eRFy_uGkAQEvJ1BAeQQy3LCwshzwMs_fqHsSYfyvCFiai0hRLkzB7Pw8hKEnxY6bBuSUICBrNa5oHXjlghb3IgH_6nnMSYdp",
            0,
            0
        ),
        # Cat Instalacion
        (
            "task_instalar_repisa",
            "cat_instalacion",
            "Instalar repisa flotante con taladro",
            "Chazos de expansión • Nivel de burbuja",
            "Fija repisas decorativas o funcionales en muros de concreto o drywall con soporte seguro.",
            "yellow",
            "Precaución requerida",
            "Existe riesgo de perforar tuberías o ductos eléctricos ocultos. Obligatorio verificar trazado de muros.",
            "Intermedia",
            "~1 a 2 h",
            38000,
            "Soportes invisibles y chazos",
            "Carga máx. 15 kg",
            "1 instalación",
            "Inmediato",
            "~50%",
            "Nunca taladre en línea recta vertical u horizontal sobre tomas, interruptores o llaves de paso.",
            "Repisa perfectamente nivelada capaz de sostener libros y adornos de forma segura.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuB5D5oVmAmuZT4voN3AarMdeplN5m6eUfuh1DNohm0t-BG6cuQFHGdZkoEEcori0H5EOv_QRjE3Yelwop-DEpFvUuBJ6h3ETHh6Zz3yZkqGJrltwsqY6L2TIQthcQeXG7OYTBcGy3m35oLaM_v3Z2xoeoSvs-k2c2zy1ilYkD6c2HDMLgFYSwsDFE45BfbZsjfPD1wh-o0yISIA59W1uqZztVyU3OHfpX6yoVZwdDbECdFYACobdwhi",
            0,
            1
        ),
        # Cat Electricidad
        (
            "task_cambiar_bombillo",
            "cat_electricidad",
            "Cambiar plafón o bombillo accesible",
            "Bombillo LED E27 • Roseta",
            "Reemplazo seguro de fuentes de luz convencionales por tecnología LED eficiente.",
            "yellow",
            "Precaución requerida",
            "Peligro de descarga eléctrica si no se corta la energía en el breaker del tablero general.",
            "Fácil",
            "~20 min",
            15000,
            "Roseta porcelana / LED",
            "Rosca estándar E27",
            "1 unidad",
            "Inmediato",
            "~75%",
            "Baja siempre el interruptor en el tablero de distribución y prueba con el switch antes de tocar.",
            "Iluminación funcional y roseta firme sin cables pelados.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBsmIvtuPilapbZVRiuZiLFOlz4J4dvLlD0gfE4QnlMDJ7wEIrNrZBWJ-FsK76I3Ii-L1LG_F-bD3JKHEifrVYmfJInwifGvQZyGvQ1Ti6LpPt5CrbBYAJRdAirxh9iuPu-s_NVoM906ycICln6Sep3eRFy_uGkAQEvJ1BAeQQy3LCwshzwMs_fqHsSYfyvCFiai0hRLkzB7Pw8hKEnxY6bBuSUICBrNa5oHXjlghb3IgH_6nnMSYdp",
            0,
            0
        ),
        (
            "task_caja_distribucion_rojo",
            "cat_electricidad",
            "Intervenir caja de tacos o cableado empotrado",
            "Tablero eléctrico • Alto voltaje",
            "Modificación de circuitos principales, breakers o acometida eléctrica.",
            "red",
            "Requiere un profesional",
            "ALTO RIESGO DE ARCO ELÉCTRICO, ELECTROCUCIÓN MORTAL O INCENDIO. Prohibido el bricolaje no certificado.",
            "Especializada",
            "N/A",
            0,
            "Certificación SEC / CONTE",
            "N/A",
            "N/A",
            "N/A",
            "0%",
            "Corta el suministro general ante chispas o sobrecalentamiento y llama a un electricista matriculado.",
            "No procedas de forma autónoma. Contrata personal calificado.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuB5D5oVmAmuZT4voN3AarMdeplN5m6eUfuh1DNohm0t-BG6cuQFHGdZkoEEcori0H5EOv_QRjE3Yelwop-DEpFvUuBJ6h3ETHh6Zz3yZkqGJrltwsqY6L2TIQthcQeXG7OYTBcGy3m35oLaM_v3Z2xoeoSvs-k2c2zy1ilYkD6c2HDMLgFYSwsDFE45BfbZsjfPD1wh-o0yISIA59W1uqZztVyU3OHfpX6yoVZwdDbECdFYACobdwhi",
            1,
            0
        ),
        # Cat Plomeria
        (
            "task_cambiar_empaque_grifo",
            "cat_plomeria",
            "Cambiar empaque o cuerito de grifo",
            "Goteo de cocina o lavamanos • Llave expansiva",
            "Detén el goteo constante cambiando los sellos de caucho o el vástago cerámico.",
            "green",
            "Reparación sencilla",
            "Se realiza sobre grifería exterior con la llave de paso local cerrada.",
            "Fácil",
            "~30 a 45 min",
            12000,
            "Empaques de nitrilo / teflón",
            "Juego universal",
            "1 grifo",
            "Inmediato",
            "~85%",
            "Cierra la llave de escuadra debajo del lavaplatos y pon un tapón en el desagüe para no perder piezas.",
            "Cierre suave del grifo con estanqueidad absoluta y cero goteo.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBsmIvtuPilapbZVRiuZiLFOlz4J4dvLlD0gfE4QnlMDJ7wEIrNrZBWJ-FsK76I3Ii-L1LG_F-bD3JKHEifrVYmfJInwifGvQZyGvQ1Ti6LpPt5CrbBYAJRdAirxh9iuPu-s_NVoM906ycICln6Sep3eRFy_uGkAQEvJ1BAeQQy3LCwshzwMs_fqHsSYfyvCFiai0hRLkzB7Pw8hKEnxY6bBuSUICBrNa5oHXjlghb3IgH_6nnMSYdp",
            0,
            1
        ),
        (
            "task_fuga_empotrada_rojo",
            "cat_plomeria",
            "Fuga en tubería interna empotrada",
            "Filtración oculta en muro • Humedad expansiva",
            "Reparación de tuberías de agua potable o residual dentro de mampostería o losas.",
            "red",
            "Requiere un profesional",
            "PELIGRO DE INUNDACIÓN GRAVE, DAÑO ESTRUCTURAL Y CORTO CIRCUITO EN DUCTOS VECINOS.",
            "Especializada",
            "N/A",
            0,
            "Detección geofónica",
            "N/A",
            "N/A",
            "N/A",
            "0%",
            "Cierra de inmediato la llave principal del contador del inmueble y contacta a un plomero certificado.",
            "No rompas paredes a ciegas. Requiere detección especializada.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCEsLDHiCC2pQBGdntWJa5ePKOOAeppP1EDpxsAw2cL-R2uZktrA41ido2kmWfsSNTB57EL8k6QlOokM_isrZzn5wej7LfRG1fg36RF4mj9ai2A02J7Jwo2ULVJfp7bhOSfUTy5cBL6sc2V-ciHhdhNOxoPCk4SwppHOcCRs_6SeAJ1WGGDoPXPg_FvnrImDltH1MF-UOywZ0ufIiP6mh-zHmBTvy7xyk3-7b7opBEG28t179_xIboM",
            1,
            0
        ),
        # Cat Muebles
        (
            "task_ajustar_bisagra",
            "cat_muebles",
            "Ajustar bisagra desalineada de mueble",
            "Puertas caídas • Calibración de tornillos",
            "Nivela puertas de gabinetes de cocina o clóset ajustando los tornillos excéntricos.",
            "green",
            "Reparación sencilla",
            "Trabajo mecánico sin herramientas peligrosas ni riesgos eléctricos.",
            "Fácil",
            "~15 a 20 min",
            8000,
            "Tornillos para madera aglomerada",
            "Hasta 4 puertas",
            "1 calibración",
            "Inmediato",
            "~95%",
            "El tornillo trasero ajusta la profundidad; el frontal mueve la puerta hacia los lados.",
            "Puertas perfectamente alineadas que cierran sin rozar ni quedar torcidas.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBsmIvtuPilapbZVRiuZiLFOlz4J4dvLlD0gfE4QnlMDJ7wEIrNrZBWJ-FsK76I3Ii-L1LG_F-bD3JKHEifrVYmfJInwifGvQZyGvQ1Ti6LpPt5CrbBYAJRdAirxh9iuPu-s_NVoM906ycICln6Sep3eRFy_uGkAQEvJ1BAeQQy3LCwshzwMs_fqHsSYfyvCFiai0hRLkzB7Pw8hKEnxY6bBuSUICBrNa5oHXjlghb3IgH_6nnMSYdp",
            0,
            0
        ),
        # Cat Baño y Cocina
        (
            "task_renovar_silicona",
            "cat_bano_cocina",
            "Sellar ducha o lavamanos con silicona",
            "Silicona antihongos • Calafateo limpio",
            "Retira el sellador ennegrecido y aplica un nuevo cordón impermeable resistente al moho.",
            "green",
            "Reparación sencilla",
            "Tarea estética de impermeabilización superficial con ventilación estándar.",
            "Fácil",
            "~1 hora",
            24000,
            "Silicona acética con fungicida",
            "Tubo de 280 ml",
            "1 cordón perimetral",
            "24 hrs secado",
            "~70%",
            "Limpia la superficie con alcohol y sécala por completo antes de aplicar el nuevo cordón.",
            "Junta limpia, brillante y 100% impermeable que previene filtraciones y moho.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCEsLDHiCC2pQBGdntWJa5ePKOOAeppP1EDpxsAw2cL-R2uZktrA41ido2kmWfsSNTB57EL8k6QlOokM_isrZzn5wej7LfRG1fg36RF4mj9ai2A02J7Jwo2ULVJfp7bhOSfUTy5cBL6sc2V-ciHhdhNOxoPCk4SwppHOcCRs_6SeAJ1WGGDoPXPg_FvnrImDltH1MF-UOywZ0ufIiP6mh-zHmBTvy7xyk3-7b7opBEG28t179_xIboM",
            0,
            1
        ),
        # Cat Mantenimiento
        (
            "task_limpiar_filtros_campana",
            "cat_mantenimiento",
            "Limpieza de filtros de campana extractora",
            "Desengrase de mallas metálicas • Agua tibia",
            "Devuelve la capacidad de succión a la campana eliminando grasa acumulada.",
            "green",
            "Reparación sencilla",
            "Limpieza preventiva con productos caseros sin desmontajes complejos.",
            "Muy fácil",
            "~30 min",
            10000,
            "Desengrasante multiusos y bicarbonato",
            "2 a 3 rejillas",
            "1 lavado",
            "Inmediato",
            "~90%",
            "Remoja los filtros en agua caliente con bicarbonato y jabón líquido durante 20 minutos.",
            "Filtros plateados y destapados con flujo de aire óptimo.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuB5D5oVmAmuZT4voN3AarMdeplN5m6eUfuh1DNohm0t-BG6cuQFHGdZkoEEcori0H5EOv_QRjE3Yelwop-DEpFvUuBJ6h3ETHh6Zz3yZkqGJrltwsqY6L2TIQthcQeXG7OYTBcGy3m35oLaM_v3Z2xoeoSvs-k2c2zy1ilYkD6c2HDMLgFYSwsDFE45BfbZsjfPD1wh-o0yISIA59W1uqZztVyU3OHfpX6yoVZwdDbECdFYACobdwhi",
            0,
            0
        ),
        (
            "task_gas_calentador_rojo",
            "cat_mantenimiento",
            "Mantenimiento o fuga en calentador de gas",
            "Red de gas combustible • Válvulas y quemador",
            "Intervención de calentadores de paso, estufas o tuberías de gas domiciliario.",
            "red",
            "Requiere un profesional",
            "RIESGO MORTAL DE INTOXICACIÓN POR MONÓXIDO DE CARBONO (CO), DEFLAGRACIÓN O EXPLOSIÓN.",
            "Especializada",
            "N/A",
            0,
            "Certificación técnica de gas",
            "N/A",
            "N/A",
            "N/A",
            "0%",
            "Si percibe olor a gas: NO encienda interruptores ni fuego, abra ventanas, cierre la llave de paso y evacúe.",
            "Servicio exclusivo de técnicos certificados por la empresa distribuidora de gas.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCEsLDHiCC2pQBGdntWJa5ePKOOAeppP1EDpxsAw2cL-R2uZktrA41ido2kmWfsSNTB57EL8k6QlOokM_isrZzn5wej7LfRG1fg36RF4mj9ai2A02J7Jwo2ULVJfp7bhOSfUTy5cBL6sc2V-ciHhdhNOxoPCk4SwppHOcCRs_6SeAJ1WGGDoPXPg_FvnrImDltH1MF-UOywZ0ufIiP6mh-zHmBTvy7xyk3-7b7opBEG28t179_xIboM",
            1,
            0
        )
    ]

    for t in tasks:
        cursor.execute("""
            INSERT OR REPLACE INTO tasks (
                id, category_id, title, short_description, full_description,
                security_level, security_badge_label, security_reason,
                difficulty, estimated_time, base_cost_cop, finish_type,
                yield_info, layers_info, drying_time, diy_savings,
                pro_tip, expected_result, image_url, requires_professional, is_popular
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, t)

    # 4. Materiales para Pintar Pared (Tiers: eco, recom, prem y base)
    materials = [
        # Base (Detalle estándar)
        ("task_pintar_pared", "base", "Pintura Tipo 1 acrílica lavable", "Galón de primera calidad con alto poder cubriente", 82000, "palette", 1),
        ("task_pintar_pared", "base", "Masilla para estuco interior", "Tubo de 250g para resanes rápidos de orificios", 8500, "construction", 1),
        ("task_pintar_pared", "base", "Lija suave al agua grano 180", "Pliego para desbaste fino y suavizado", 2000, "texture", 1),
        ("task_pintar_pared", "base", "Plástico protector de piso (2x3m)", "Película de polietileno calibre 2", 4000, "layers", 1),
        ("task_pintar_pared", "base", "Agua limpia para dilución (10%)", "Para mezcla homogénea del vinilo", 0, "water_drop", 1),

        # Económica ($98.000)
        ("task_pintar_pared", "eco", "Galón de vinilo estándar Tipo 2", "1 galón / 3.78 L • Rendimiento 20-25 m²", 58000, "check_circle", 1),
        ("task_pintar_pared", "eco", "Rodillo básico de felpa sintética", "Rodillo 9 pulgadas para uso doméstico", 15000, "check_circle", 1),
        ("task_pintar_pared", "eco", "Cinta de enmascarar estándar 18mm", "Adhesivo suave para zócalos", 5000, "check_circle", 1),
        ("task_pintar_pared", "eco", "Tubo estuco acrílico pequeño 200g", "Para tapar pequeñas grietas", 8000, "check_circle", 1),
        ("task_pintar_pared", "eco", "Pliego de plástico protector delgado", "Protección ligera para piso", 12000, "check_circle", 1),

        # Recomendada ($148.500)
        ("task_pintar_pared", "recom", "Galón de vinilo acrílico Tipo 1", "1 galón / 3.78 L • Rendimiento 25-30 m²", 82000, "colors", 1),
        ("task_pintar_pared", "recom", "Rodillo felpa 9\" antigota + bandeja", "Mango ergonómico con rosca para extensión", 24500, "brush", 1),
        ("task_pintar_pared", "recom", "Brocha cerda angular suave 2.5\"", "Corte perfecto de esquinas y marcos", 14000, "brush", 1),
        ("task_pintar_pared", "recom", "Cinta pintor azul resistente UV 24mm", "No deja residuos de pegante ni levanta pintura", 12000, "line_weight", 1),
        ("task_pintar_pared", "recom", "Masilla estuco interior 450g + espátula", "Masilla lista para usar y lija suave #180", 16000, "handyman", 1),

        # Prémium ($215.000)
        ("task_pintar_pared", "prem", "Galón esmalte al agua antibacterial", "1 galón • Máxima lavabilidad y protección anti-hongos", 128000, "check_circle", 1),
        ("task_pintar_pared", "prem", "Kit rodillo microfibra pro + extensión 1.2m", "Acabado ultra sedoso sin salpicaduras", 38000, "check_circle", 1),
        ("task_pintar_pared", "prem", "Cinta precisión bordes nítidos 24mm", "Tecnología Bloqueador de Pintura (PaintBlock)", 19000, "check_circle", 1),
        ("task_pintar_pared", "prem", "Pasta resanadora ultra-rápida + espátula inox", "Acabado espejo en 15 minutos", 18000, "check_circle", 1),
        ("task_pintar_pared", "prem", "Manta textil absorbente plastificada 4x4m", "Reutilizable y anti-deslizante", 12000, "check_circle", 1),

        # Otras tareas
        ("task_resanar_agujeros", "recom", "Tubo estuco plástico para interiores 250g", "Masilla blanca lista para aplicar", 8500, "construction", 1),
        ("task_resanar_agujeros", "recom", "Lija al agua grano fino #220", "Pliego para acabado suave al tacto", 2000, "texture", 1),
        ("task_resanar_agujeros", "recom", "Espátula plástica flexible de 2 pulgadas", "Ideal para no rayar la pared", 5500, "handyman", 1),
        ("task_instalar_repisa", "recom", "Juego de 4 chazos de expansión 1/4\" con tornillos", "Para muro de ladrillo o concreto", 6000, "construction", 1),
        ("task_instalar_repisa", "recom", "Broca para mampostería 1/4\" punta tungsteno", "Para perforación limpia sin desmoronar", 9500, "build", 1),
        ("task_cambiar_empaque_grifo", "recom", "Juego de cueritos y empaques surtidos de nitrilo", "Resistentes al agua caliente y fría", 4500, "valve", 1),
        ("task_cambiar_empaque_grifo", "recom", "Cinta de teflón para fontanería 1/2\"", "Sellado de roscas antifugas", 3000, "texture", 1),
        ("task_renovar_silicona", "recom", "Tubo de silicona acética antihongos blanca 280ml", "Protección contra moho y humedad por 5 años", 18000, "shower", 1),
        ("task_renovar_silicona", "recom", "Cinta de enmascarar para delimitar bordes", "Para cordón recto y estético", 4500, "line_weight", 1)
    ]

    cursor.execute("DELETE FROM task_materials")
    for mat in materials:
        cursor.execute("""
            INSERT INTO task_materials (task_id, tier, name, description, unit_price_cop, icon, is_essential)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, mat)

    # 5. Herramientas
    tools = [
        ("task_pintar_pared", "Rodillo con felpa antigoteo", "check_circle", 0),
        ("task_pintar_pared", "Brocha 2.5\" corte angular", "check_circle", 0),
        ("task_pintar_pared", "Bandeja plástica reforzada", "check_circle", 0),
        ("task_pintar_pared", "Espátula metálica (resane)", "check_circle", 1),
        ("task_pintar_pared", "Cinta de enmascarar azul", "check_circle", 1),
        ("task_resanar_agujeros", "Espátula de 2\" o 3\"", "check_circle", 1),
        ("task_resanar_agujeros", "Trapo húmedo limpio", "check_circle", 1),
        ("task_instalar_repisa", "Taladro con percutor", "check_circle", 0),
        ("task_instalar_repisa", "Nivel de burbuja", "check_circle", 1),
        ("task_instalar_repisa", "Cinta métrica y lápiz", "check_circle", 1),
        ("task_cambiar_bombillo", "Escalera de tijera firme", "check_circle", 1),
        ("task_cambiar_bombillo", "Destornillador de pala o estrella", "check_circle", 1),
        ("task_cambiar_empaque_grifo", "Llave expansiva o ajustable", "check_circle", 1),
        ("task_cambiar_empaque_grifo", "Destornillador fino", "check_circle", 1),
        ("task_ajustar_bisagra", "Destornillador de estrella #2", "check_circle", 1),
        ("task_renovar_silicona", "Pistola para silicona de calafateo", "check_circle", 0),
        ("task_renovar_silicona", "Bisturí o cuchilla para retirar silicona vieja", "check_circle", 1)
    ]

    cursor.execute("DELETE FROM task_tools")
    for tool in tools:
        cursor.execute("""
            INSERT INTO task_tools (task_id, name, icon, is_common)
            VALUES (?, ?, ?, ?)
        """, tool)

    # 6. Pasos de Ejecución
    steps = [
        # Pintar pared
        ("task_pintar_pared", 1, "Despeje y protección", "Retira muebles, cuadros y tapas de tomas eléctricas. Cubre el piso con el plástico y fija zócalos con cinta.", "Asegúrate de que el plástico no resbale al caminar."),
        ("task_pintar_pared", 2, "Resane y lijado previo", "Aplica estuco en agujeros o rayones con la espátula. Deja secar 45 min y lija suavemente con grano #180.", "Pasa un paño seco para eliminar el polvo antes de pintar."),
        ("task_pintar_pared", 3, "Recorte de bordes", "Con la brocha angular de 2.5\", pinta una franja de 5 cm a lo largo del techo, zócalos y esquinas.", "Mantén la brocha húmeda sin sobrecargar pintura."),
        ("task_pintar_pared", 4, "Primera mano con rodillo", "Carga el rodillo en la bandeja y aplica en la pared dibujando una 'W' o 'M' para distribuir parejo.", "Trabaja por secciones de 1 metro cuadrado sin presionar en exceso."),
        ("task_pintar_pared", 5, "Segunda mano y acabado final", "Espera 2 a 3 horas de secado y aplica la segunda mano uniforme en pasadas verticales continuas.", "Retira la cinta de enmascarar mientras la pintura aún esté ligeramente húmeda."),

        # Resanar agujeros
        ("task_resanar_agujeros", 1, "Limpiar el orificio", "Retira el polvo o restos de yeso suelto con la punta de la espátula.", "Un orificio limpio garantiza adherencia duradera."),
        ("task_resanar_agujeros", 2, "Cargar y presionar estuco", "Toma una pequeña cantidad de masilla y presiona firmemente rellenando la cavidad.", "Aplica en ángulo de 45°."),
        ("task_resanar_agujeros", 3, "Nivelar al ras", "Pasa la espátula limpia horizontalmente para retirar todo sobrante.", "Evita dejar montículos grandes que cuesten lijar."),
        ("task_resanar_agujeros", 4, "Lijado suave", "Una vez seco al tacto (45 min), lija con lija #220 con movimientos circulares hasta sentir plano.", "Limpia el polvillo antes de retocar color."),

        # Cambiar empaque grifo
        ("task_cambiar_empaque_grifo", 1, "Cerrar llave de paso", "Cierra la llave de escuadra debajo del mueble o la llave general del baño.", "Abre el grifo para verificar que no salga más agua."),
        ("task_cambiar_empaque_grifo", 2, "Desmontar la manija", "Retira la tapita embellecedora y suelta el tornillo central con destornillador.", "Pon el tapón en el desagüe para no perder piezas."),
        ("task_cambiar_empaque_grifo", 3, "Extraer el vástago y cambiar empaque", "Desenrosca el vástago con llave expansiva y reemplaza el cuerito o anillo de caucho desgastado.", "Aplica una vuelta de teflón en la rosca si es necesario."),
        ("task_cambiar_empaque_grifo", 4, "Reensamblar y probar", "Vuelve a armar todo, abre la llave de paso y comprueba que cierre herméticamente.", "Verifica que no gotee ni por la base ni por la boquilla.")
    ]

    cursor.execute("DELETE FROM task_steps")
    for stp in steps:
        cursor.execute("""
            INSERT INTO task_steps (task_id, step_number, title, instructions, safety_tip)
            VALUES (?, ?, ?, ?, ?)
        """, stp)

    # 7. Proyectos y Favoritos de Prueba para el usuario Dylan
    cursor.execute("DELETE FROM user_projects WHERE user_id = ?", (user_id,))
    
    # Proyecto en progreso: Pintar sala principal
    cursor.execute("""
        INSERT INTO user_projects (
            user_id, task_id, project_name, phase_name, status,
            progress_percent, area_m2, tier_selected, calculated_cost_cop,
            notes, is_favorite
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        "task_pintar_pared",
        "Pintar sala principal",
        "Fase 2: Preparación y masilla",
        "en_progreso",
        65,
        14.5,
        "recom",
        185000,
        "Comprar el vinilo tono marfil en la ferretería central el sábado.",
        1
    ))

    # Favorito 1: Cambiar empaque grifo
    cursor.execute("""
        INSERT INTO user_projects (
            user_id, task_id, project_name, phase_name, status,
            progress_percent, area_m2, tier_selected, calculated_cost_cop,
            notes, is_favorite
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        "task_cambiar_empaque_grifo",
        "Cambiar empaque grifo lavaplatos",
        "Planeado para fin de mes",
        "planeado",
        0,
        1.0,
        "recom",
        12000,
        "Revisar si la llave de escuadra gira bien antes de soltar.",
        1
    ))

    # Favorito 2: Tapar huecos de puntilla
    cursor.execute("""
        INSERT INTO user_projects (
            user_id, task_id, project_name, phase_name, status,
            progress_percent, area_m2, tier_selected, calculated_cost_cop,
            notes, is_favorite
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        "task_resanar_agujeros",
        "Tapar huecos de puntilla en pasillo",
        "Materiales listos",
        "planeado",
        0,
        1.0,
        "recom",
        18000,
        "Quedaron 6 orificios tras retirar los cuadros.",
        1
    ))

    conn.commit()
    conn.close()
    print("Base de datos de CasaLista inicializada y sembrada con éxito.")

if __name__ == "__main__":
    from app.database import init_db
    init_db()
    seed_database()
