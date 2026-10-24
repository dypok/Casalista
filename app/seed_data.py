from app.database import get_db_connection
from app.auth import hash_password

def seed_database():
    """Siembra los datos iniciales completos para CasaLista en todos sus módulos."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Usuario de prueba principal (Karla Polanco)
    existing_user = cursor.execute("SELECT id FROM users WHERE email = 'prueba@casalista.co'").fetchone()
    if not existing_user:
        hashed_pwd = hash_password("casalista123")
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, city)
            VALUES (?, ?, ?, ?)
        """, ("Karla Polanco", "prueba@casalista.co", hashed_pwd, "Bogotá, D.C."))
        user_id = cursor.lastrowid
    else:
        user_id = existing_user["id"]
        cursor.execute("UPDATE users SET name = ? WHERE id = ?", ("Karla Polanco", user_id))

    # 2. Las 8 Categorías Oficiales
    categories = [
        ("cat_pintura", "Pintura y acabados", "Paredes, techos y marcos", "format_paint", "Dificultad básica • Est. COP", "info", "facil", "paredes techos marcos rodillo pintura brochas lija esmalte", 1),
        ("cat_paredes", "Paredes y pequeños daños", "Resanes, fisuras y huecos", "handyman", "Secado rápido • Bricolaje fácil", "info", "facil", "resanes fisuras huecos masilla yeso espatula grietas drywall", 2),
        ("cat_instalacion", "Instalación y organización", "Repisas, cuadros y cortineros", "shelves", "Requiere brocas y nivel", "caution", "intermedio", "repisas cuadros cortineros taladro anclajes chazos fijacion", 3),
        ("cat_electricidad", "Electricidad básica", "Interruptores y plafones", "lightbulb", "Cortar breaker antes", "warning", "precaucion", "electricidad interruptores plafones tomas breakers bombillo roseta", 4),
        ("cat_plomeria", "Plomería menor", "Fugas de sifón, empaques y grifos", "build", "Llave de paso requerida", "caution", "intermedio", "plomeria fugas sifon empaques grifos agua llave goteo teflon", 5),
        ("cat_muebles", "Muebles y puertas", "Ajuste de bisagras y chapas", "door_front", "Destornillador + lubricación", "info", "facil", "muebles puertas bisagras chapas cerradura lubricante madera rieles", 6),
        ("cat_bano_cocina", "Baño y cocina", "Silicona, duchas y rejillas", "shower", "Prevención antihongos", "caution", "intermedio", "bano cocina silicona duchas rejillas sellado humedad calafateo sanitario", 7),
        ("cat_mantenimiento", "Mantenimiento preventivo", "Filtros, campanas y techos", "shield", "Inspección periódica", "info", "facil", "mantenimiento preventivo filtros campanas revision humedad estufa", 8)
    ]

    for cat in categories:
        cursor.execute("""
            INSERT OR REPLACE INTO categories (id, name, subtitle, icon, badge_text, badge_type, difficulty_tag, keywords, order_num)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, cat)

    # 3. Catálogo Completo de Tareas (24 Tareas en las 8 Categorías)
    tasks = [
        # --- CAT 1: PINTURA Y ACABADOS ---
        (
            "task_pintar_pared", "cat_pintura", "Pintar una pared interior",
            "Herramientas básicas • Rodillo y cinta",
            "Aprende a calcular la pintura exacta, preparar la superficie, resanar imperfecciones y aplicar manos uniformes para renovar cualquier habitación.",
            "green", "Reparación sencilla",
            "Se realiza sobre piso firme a nivel del suelo sin riesgo de caídas ni exposición a voltajes peligrosos.",
            "Fácil", "~3 a 4 h", 45000, "Vinilo Tipo 1 Satinado",
            "~25 m²/gal", "2 capas", "2 a 4 hrs", "~65%",
            "Ventila adecuadamente el espacio y protege rodapiés y tomacorrientes antes de comenzar para evitar manchas indeseadas y reducir tiempo de limpieza.",
            "Pared lisa, sin marcas de rodillo ni sombras de empalme, con bordes perfectamente definidos.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuDkGFETcHQ3pfGR2EJTTRntA0g0QNXshRyMmOPh9zcNomqvrVm6ZiONoetRBO9MofXbkyjGhZqK3nYKueRz_N1Ti6mXCegllLmOYnq-LfIsYJLuTQpdNOqoMtBUaL834t1Dz5aztrRYxVeCq_MPRYsYqCvqQDmNIMQ6RqrmrYVvWrkq0_5m_GHZ4RR94gDmVCtTcm_BIAw5DHEV9JjkFNE84g6OluagACeesPO63mY4jVfMZT_T_rD6",
            0, 1
        ),
        (
            "task_retocar_zocalos", "cat_pintura", "Retocar zócalos y molduras",
            "Pintura perimetral • Brocha de recorte",
            "Repara raspones, golpes y manchas de suciedad en zócalos de madera, yeso o cemento con brocha fina.",
            "green", "Reparación sencilla",
            "Trabajo seguro a ras de suelo sin herramientas mecánicas de riesgo.",
            "Fácil", "~1 a 2 h", 25000, "Esmalte al agua",
            "~30 m lineales/cuarto", "2 capas", "1 a 2 hrs", "~70%",
            "Usa cinta de enmascarar en el piso para asegurar una línea recta perfecta y evitar manchar la baldosa o alfombra.",
            "Bordes limpios y zócalos protegidos sin goteos ni manchas en el piso.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBsmIvtuPilapbZVRiuZiLFOlz4J4dvLlD0gfE4QnlMDJ7wEIrNrZBWJ-FsK76I3Ii-L1LG_F-bD3JKHEifrVYmfJInwifGvQZyGvQ1Ti6LpPt5CrbBYAJRdAirxh9iuPu-s_NVoM906ycICln6Sep3eRFy_uGkAQEvJ1BAeQQy3LCwshzwMs_fqHsSYfyvCFiai0hRLkzB7Pw8hKEnxY6bBuSUICBrNa5oHXjlghb3IgH_6nnMSYdp",
            0, 0
        ),
        (
            "task_pintar_puerta", "cat_pintura", "Pintar o barnizar puerta interior",
            "Acabado satinado • Rodillo de espuma",
            "Renueva la apariencia de puertas entamboradas o de madera maciza aplicando laca o esmalte sintético.",
            "green", "Reparación sencilla",
            "Labor ergonómica; se recomienda desmontar la hoja o calzarla firmemente con cuña.",
            "Fácil", "~2 a 3 h", 38000, "Esmalte sintético brillante",
            "1 puerta por litro", "2 capas", "4 a 6 hrs", "~60%",
            "Lija suavemente en el sentido de las vetas de la madera para que la nueva capa tenga adherencia impecable.",
            "Puerta sin marcas de brocha, con brillo parejo y superficie sedosa al tacto.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCEsLDHiCC2pQBGdntWJa5ePKOOAeppP1EDpxsAw2cL-R2uZktrA41ido2kmWfsSNTB57EL8k6QlOokM_isrZzn5wej7LfRG1fg36RF4mj9ai2A02J7Jwo2ULVJfp7bhOSfUTy5cBL6sc2V-ciHhdhNOxoPCk4SwppHOcCRs_6SeAJ1WGGDoPXPg_FvnrImDltH1MF-UOywZ0ufIiP6mh-zHmBTvy7xyk3-7b7opBEG28t179_xIboM",
            0, 0
        ),

        # --- CAT 2: PAREDES Y PEQUEÑOS DAÑOS ---
        (
            "task_resanar_agujeros", "cat_paredes", "Tapar huecos de puntilla o chazo",
            "Estuco plástico interior • Espátula",
            "Rellena pequeños orificios dejados por cuadros, repisas o clavos en muros de mampostería o drywall.",
            "green", "Reparación sencilla",
            "No compromete la estructura del muro y los materiales de masilla no son tóxicos.",
            "Muy fácil", "~30 a 45 min", 18000, "Estuco plástico",
            "Hasta 25 huecos por tubo", "1 a 2 capas", "1 hr", "~80%",
            "Aplica la masilla en ángulo de 45° y retira el exceso al ras para minimizar el lijado posterior.",
            "Superficie completamente plana y lista para aplicar pintura de retoque.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuDkGFETcHQ3pfGR2EJTTRntA0g0QNXshRyMmOPh9zcNomqvrVm6ZiONoetRBO9MofXbkyjGhZqK3nYKueRz_N1Ti6mXCegllLmOYnq-LfIsYJLuTQpdNOqoMtBUaL834t1Dz5aztrRYxVeCq_MPRYsYqCvqQDmNIMQ6RqrmrYVvWrkq0_5m_GHZ4RR94gDmVCtTcm_BIAw5DHEV9JjkFNE84g6OluagACeesPO63mY4jVfMZT_T_rD6",
            0, 1
        ),
        (
            "task_reparar_grieta_superficial", "cat_paredes", "Reparar fisura superficial en estuco",
            "Cinta de malla de fibra • Masilla elastomérica",
            "Corrige micro-fisuras cosméticas menores a 1 mm en muros de pañete o yeso sin daño estructural.",
            "yellow", "Precaución requerida",
            "Requiere verificar que la fisura no atraviese columnas o vigas de carga estructural.",
            "Moderada", "~1 a 2 h", 32000, "Masilla elástica y malla",
            "~5 metros lineales", "2 capas", "3 hrs", "~60%",
            "Si la grieta mide más de 2 mm o se ensancha con el tiempo, consulta a un ingeniero civil.",
            "Fisura sellada elásticamente que previene reaparición de marcas con dilataciones térmicas.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBsmIvtuPilapbZVRiuZiLFOlz4J4dvLlD0gfE4QnlMDJ7wEIrNrZBWJ-FsK76I3Ii-L1LG_F-bD3JKHEifrVYmfJInwifGvQZyGvQ1Ti6LpPt5CrbBYAJRdAirxh9iuPu-s_NVoM906ycICln6Sep3eRFy_uGkAQEvJ1BAeQQy3LCwshzwMs_fqHsSYfyvCFiai0hRLkzB7Pw8hKEnxY6bBuSUICBrNa5oHXjlghb3IgH_6nnMSYdp",
            0, 0
        ),
        (
            "task_fijar_esquinero_drywall", "cat_paredes", "Reparar esquinero golpeado en drywall",
            "Esquinero metálico • Masilla de drywall",
            "Corrige esquinas abolladas por muebles o maletas en tabiques divisorios de yeso-cartón.",
            "yellow", "Precaución requerida",
            "Uso de bisturí y manipulación de bordes metálicos; requiere uso de guantes de protección.",
            "Moderada", "~1.5 h", 28000, "Masilla tipo Joint Compound",
            "1 esquinero de 2.4 m", "2 capas", "4 hrs", "~65%",
            "Retira el metal doblado antes de empastar para evitar que se despegue la masilla con el tiempo.",
            "Esquina a 90 grados sólida, recta y perfectamente perfilada.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCEsLDHiCC2pQBGdntWJa5ePKOOAeppP1EDpxsAw2cL-R2uZktrA41ido2kmWfsSNTB57EL8k6QlOokM_isrZzn5wej7LfRG1fg36RF4mj9ai2A02J7Jwo2ULVJfp7bhOSfUTy5cBL6sc2V-ciHhdhNOxoPCk4SwppHOcCRs_6SeAJ1WGGDoPXPg_FvnrImDltH1MF-UOywZ0ufIiP6mh-zHmBTvy7xyk3-7b7opBEG28t179_xIboM",
            0, 0
        ),

        # --- CAT 3: INSTALACIÓN Y ORGANIZACIÓN ---
        (
            "task_instalar_repisa", "cat_instalacion", "Instalar repisa flotante con taladro",
            "Chazos de expansión • Nivel de burbuja",
            "Fija repisas decorativas o funcionales en muros de concreto, ladrillo o drywall con soporte seguro.",
            "yellow", "Precaución requerida",
            "Existe riesgo de perforar tuberías o ductos eléctricos ocultos. Obligatorio verificar trazado de muros.",
            "Intermedia", "~1 a 2 h", 38000, "Soportes invisibles y chazos",
            "Carga máx. 15 kg", "1 instalación", "Inmediato", "~50%",
            "Nunca taladres en línea vertical u horizontal exacta sobre tomas, interruptores o llaves de paso.",
            "Repisa perfectamente nivelada capaz de sostener libros y adornos de forma segura.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuB5D5oVmAmuZT4voN3AarMdeplN5m6eUfuh1DNohm0t-BG6cuQFHGdZkoEEcori0H5EOv_QRjE3Yelwop-DEpFvUuBJ6h3ETHh6Zz3yZkqGJrltwsqY6L2TIQthcQeXG7OYTBcGy3m35oLaM_v3Z2xoeoSvs-k2c2zy1ilYkD6c2HDMLgFYSwsDFE45BfbZsjfPD1wh-o0yISIA59W1uqZztVyU3OHfpX6yoVZwdDbECdFYACobdwhi",
            0, 1
        ),
        (
            "task_colgar_cuadros", "cat_instalacion", "Colgar cuadros y espejos con anclajes",
            "Ganchos adhesivos o clavos de acero • Nivel",
            "Instala cuadros, marcos familiares y espejos medianos sin dañar muros con anclajes adecuados.",
            "green", "Reparación sencilla",
            "Carga liviana (<5 kg) que no requiere perforación agresiva ni compromete redes internas.",
            "Muy fácil", "~30 min", 12000, "Ganchos fijación limpia",
            "Hasta 6 cuadros", "1 montaje", "Inmediato", "~85%",
            "Coloca el centro del cuadro a la altura promedio de los ojos (1.50 metros desde el piso).",
            "Galería de cuadros nivelada y firmemente sujeta sin torceduras.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuDkGFETcHQ3pfGR2EJTTRntA0g0QNXshRyMmOPh9zcNomqvrVm6ZiONoetRBO9MofXbkyjGhZqK3nYKueRz_N1Ti6mXCegllLmOYnq-LfIsYJLuTQpdNOqoMtBUaL834t1Dz5aztrRYxVeCq_MPRYsYqCvqQDmNIMQ6RqrmrYVvWrkq0_5m_GHZ4RR94gDmVCtTcm_BIAw5DHEV9JjkFNE84g6OluagACeesPO63mY4jVfMZT_T_rD6",
            0, 0
        ),
        (
            "task_instalar_cortinero", "cat_instalacion", "Instalar barra o soporte de cortina",
            "Barra metálica • Soportes dobles y chazos",
            "Monta barras de cortinas pesadas o visillos en ventana de alcoba o sala con anclajes resistentes.",
            "yellow", "Precaución requerida",
            "Trabajo en altura de escalera (2 a 2.5 metros) y perforación con taladro en dintel de ventana.",
            "Intermedia", "~1.5 h", 34000, "Chazos mariposa / broca 5/16",
            "Ventana de 1.5 a 2.2 m", "1 barra", "Inmediato", "~55%",
            "Usa chazos mariposa si el dintel está construido en drywall para evitar que el peso tire la barra.",
            "Barra firme y cortinas con desplazamiento fluido sin pandeo central.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBsmIvtuPilapbZVRiuZiLFOlz4J4dvLlD0gfE4QnlMDJ7wEIrNrZBWJ-FsK76I3Ii-L1LG_F-bD3JKHEifrVYmfJInwifGvQZyGvQ1Ti6LpPt5CrbBYAJRdAirxh9iuPu-s_NVoM906ycICln6Sep3eRFy_uGkAQEvJ1BAeQQy3LCwshzwMs_fqHsSYfyvCFiai0hRLkzB7Pw8hKEnxY6bBuSUICBrNa5oHXjlghb3IgH_6nnMSYdp",
            0, 0
        ),

        # --- CAT 4: ELECTRICIDAD BÁSICA ---
        (
            "task_cambiar_bombillo", "cat_electricidad", "Cambiar plafón o bombillo accesible",
            "Bombillo LED E27 • Roseta",
            "Reemplazo seguro de fuentes de luz convencionales por tecnología LED eficiente.",
            "yellow", "Precaución requerida",
            "Peligro de descarga eléctrica si no se corta la energía en el breaker del tablero general.",
            "Fácil", "~20 min", 15000, "Roseta porcelana / LED",
            "Rosca estándar E27", "1 unidad", "Inmediato", "~75%",
            "Baja siempre el interruptor en el tablero de distribución y prueba con el switch antes de tocar.",
            "Iluminación funcional y roseta firme sin cables pelados.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBsmIvtuPilapbZVRiuZiLFOlz4J4dvLlD0gfE4QnlMDJ7wEIrNrZBWJ-FsK76I3Ii-L1LG_F-bD3JKHEifrVYmfJInwifGvQZyGvQ1Ti6LpPt5CrbBYAJRdAirxh9iuPu-s_NVoM906ycICln6Sep3eRFy_uGkAQEvJ1BAeQQy3LCwshzwMs_fqHsSYfyvCFiai0hRLkzB7Pw8hKEnxY6bBuSUICBrNa5oHXjlghb3IgH_6nnMSYdp",
            0, 0
        ),
        (
            "task_cambiar_interruptor", "cat_electricidad", "Cambiar interruptor o placa de pared",
            "Módulo balancín 10A • Placa blanca",
            "Sustituye interruptores desgastados, con falso contacto o estéticamente deteriorados.",
            "yellow", "Precaución requerida",
            "Requiere corte obligatorio de energía y verificar con buscapolo que no haya tensión residual.",
            "Intermedia", "~35 min", 22000, "Interruptor unipolar norma RETIE",
            "1 punto de luz", "1 placa", "Inmediato", "~70%",
            "Toma una foto con tu teléfono a los cables antes de desconectar para conectar en los mismos bornes.",
            "Accionamiento suave con sonido nítido de contacto y placa perfectamente alineada.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuB5D5oVmAmuZT4voN3AarMdeplN5m6eUfuh1DNohm0t-BG6cuQFHGdZkoEEcori0H5EOv_QRjE3Yelwop-DEpFvUuBJ6h3ETHh6Zz3yZkqGJrltwsqY6L2TIQthcQeXG7OYTBcGy3m35oLaM_v3Z2xoeoSvs-k2c2zy1ilYkD6c2HDMLgFYSwsDFE45BfbZsjfPD1wh-o0yISIA59W1uqZztVyU3OHfpX6yoVZwdDbECdFYACobdwhi",
            0, 0
        ),
        (
            "task_caja_distribucion_rojo", "cat_electricidad", "Intervenir caja de tacos o cableado empotrado",
            "Tablero eléctrico • Alto voltaje",
            "Modificación de circuitos principales, breakers o acometida eléctrica.",
            "red", "Requiere un profesional",
            "ALTO RIESGO DE ARCO ELÉCTRICO, ELECTROCUCIÓN MORTAL O INCENDIO. Prohibido el bricolaje no certificado.",
            "Especializada", "N/A", 0, "Certificación SEC / CONTE",
            "N/A", "N/A", "N/A", "0%",
            "Corta el suministro general ante chispas o sobrecalentamiento y llama a un electricista matriculado.",
            "No procedas de forma autónoma. Contrata personal calificado.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuB5D5oVmAmuZT4voN3AarMdeplN5m6eUfuh1DNohm0t-BG6cuQFHGdZkoEEcori0H5EOv_QRjE3Yelwop-DEpFvUuBJ6h3ETHh6Zz3yZkqGJrltwsqY6L2TIQthcQeXG7OYTBcGy3m35oLaM_v3Z2xoeoSvs-k2c2zy1ilYkD6c2HDMLgFYSwsDFE45BfbZsjfPD1wh-o0yISIA59W1uqZztVyU3OHfpX6yoVZwdDbECdFYACobdwhi",
            1, 0
        ),

        # --- CAT 5: PLOMERÍA MENOR ---
        (
            "task_cambiar_empaque_grifo", "cat_plomeria", "Cambiar empaque o cuerito de grifo",
            "Goteo de cocina o lavamanos • Llave expansiva",
            "Detén el goteo constante cambiando los sellos de caucho o el vástago cerámico.",
            "green", "Reparación sencilla",
            "Se realiza sobre grifería exterior con la llave de paso local cerrada.",
            "Fácil", "~30 a 45 min", 12000, "Empaques de nitrilo / teflón",
            "Juego universal", "1 grifo", "Inmediato", "~85%",
            "Cierra la llave de escuadra debajo del lavaplatos y pon un tapón en el desagüe para no perder piezas.",
            "Cierre suave del grifo con estanqueidad absoluta y cero goteo.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBsmIvtuPilapbZVRiuZiLFOlz4J4dvLlD0gfE4QnlMDJ7wEIrNrZBWJ-FsK76I3Ii-L1LG_F-bD3JKHEifrVYmfJInwifGvQZyGvQ1Ti6LpPt5CrbBYAJRdAirxh9iuPu-s_NVoM906ycICln6Sep3eRFy_uGkAQEvJ1BAeQQy3LCwshzwMs_fqHsSYfyvCFiai0hRLkzB7Pw8hKEnxY6bBuSUICBrNa5oHXjlghb3IgH_6nnMSYdp",
            0, 1
        ),
        (
            "task_limpiar_sifon", "cat_plomeria", "Limpiar o desatorar sifón bajo lavamanos",
            "Sifón plástico en P • Balde y guantes",
            "Elimina malos olores y atascos de agua acumulada retirando el depósito inferior del sifón.",
            "green", "Reparación sencilla",
            "Operación mecánica manual en desagüe; no requiere químicos cáusticos ni herramienta pesada.",
            "Fácil", "~25 min", 16000, "Empaques cónicos de repuesto",
            "1 sifón", "1 servicio", "Inmediato", "~90%",
            "Coloca siempre un balde debajo antes de desenroscar la tuerca para recibir el agua estancada.",
            "Desagüe rápido y eliminación total de burbujas y malos olores.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCEsLDHiCC2pQBGdntWJa5ePKOOAeppP1EDpxsAw2cL-R2uZktrA41ido2kmWfsSNTB57EL8k6QlOokM_isrZzn5wej7LfRG1fg36RF4mj9ai2A02J7Jwo2ULVJfp7bhOSfUTy5cBL6sc2V-ciHhdhNOxoPCk4SwppHOcCRs_6SeAJ1WGGDoPXPg_FvnrImDltH1MF-UOywZ0ufIiP6mh-zHmBTvy7xyk3-7b7opBEG28t179_xIboM",
            0, 0
        ),
        (
            "task_fuga_empotrada_rojo", "cat_plomeria", "Fuga en tubería interna empotrada",
            "Filtración oculta en muro • Humedad expansiva",
            "Reparación de tuberías de agua potable o residual dentro de mampostería o losas.",
            "red", "Requiere un profesional",
            "PELIGRO DE INUNDACIÓN GRAVE, DAÑO ESTRUCTURAL Y CORTO CIRCUITO EN DUCTOS VECINOS.",
            "Especializada", "N/A", 0, "Detección geofónica",
            "N/A", "N/A", "N/A", "0%",
            "Cierra de inmediato la llave principal del contador del inmueble y contacta a un plomero certificado.",
            "No rompas paredes a ciegas. Requiere detección especializada.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCEsLDHiCC2pQBGdntWJa5ePKOOAeppP1EDpxsAw2cL-R2uZktrA41ido2kmWfsSNTB57EL8k6QlOokM_isrZzn5wej7LfRG1fg36RF4mj9ai2A02J7Jwo2ULVJfp7bhOSfUTy5cBL6sc2V-ciHhdhNOxoPCk4SwppHOcCRs_6SeAJ1WGGDoPXPg_FvnrImDltH1MF-UOywZ0ufIiP6mh-zHmBTvy7xyk3-7b7opBEG28t179_xIboM",
            1, 0
        ),

        # --- CAT 6: MUEBLES Y PUERTAS ---
        (
            "task_ajustar_bisagra", "cat_muebles", "Ajustar bisagra desalineada de mueble",
            "Puertas caídas • Calibración de tornillos",
            "Nivela puertas de gabinetes de cocina o clóset ajustando los tornillos excéntricos.",
            "green", "Reparación sencilla",
            "Trabajo mecánico sin herramientas peligrosas ni riesgos eléctricos.",
            "Fácil", "~15 a 20 min", 8000, "Tornillos para madera aglomerada",
            "Hasta 4 puertas", "1 calibración", "Inmediato", "~95%",
            "El tornillo trasero ajusta la profundidad; el frontal mueve la puerta hacia los lados.",
            "Puertas perfectamente alineadas que cierran sin rozar ni quedar torcidas.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBsmIvtuPilapbZVRiuZiLFOlz4J4dvLlD0gfE4QnlMDJ7wEIrNrZBWJ-FsK76I3Ii-L1LG_F-bD3JKHEifrVYmfJInwifGvQZyGvQ1Ti6LpPt5CrbBYAJRdAirxh9iuPu-s_NVoM906ycICln6Sep3eRFy_uGkAQEvJ1BAeQQy3LCwshzwMs_fqHsSYfyvCFiai0hRLkzB7Pw8hKEnxY6bBuSUICBrNa5oHXjlghb3IgH_6nnMSYdp",
            0, 0
        ),
        (
            "task_lubricar_cerradura", "cat_muebles", "Lubricar y desatorar cerradura de puerta",
            "Grafito en polvo o lubricante seco • Sin grasa",
            "Restaura el giro suave de la llave en chapas principales que se traban o están resecas.",
            "green", "Reparación sencilla",
            "Mantenimiento no invasivo por la ranura del cilindro.",
            "Muy fácil", "~15 min", 14000, "Grafito en polvo para cerraduras",
            "Hasta 5 cerraduras", "1 aplicación", "Inmediato", "~85%",
            "Nunca uses aceite de cocina ni grasa espesa, ya que atrapan polvo y dañan los pernos internos.",
            "Llave entra suavemente y el pestillo gira sin resistencia ni esfuerzo.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuDkGFETcHQ3pfGR2EJTTRntA0g0QNXshRyMmOPh9zcNomqvrVm6ZiONoetRBO9MofXbkyjGhZqK3nYKueRz_N1Ti6mXCegllLmOYnq-LfIsYJLuTQpdNOqoMtBUaL834t1Dz5aztrRYxVeCq_MPRYsYqCvqQDmNIMQ6RqrmrYVvWrkq0_5m_GHZ4RR94gDmVCtTcm_BIAw5DHEV9JjkFNE84g6OluagACeesPO63mY4jVfMZT_T_rD6",
            0, 0
        ),
        (
            "task_reparar_corredera_cajon", "cat_muebles", "Cambiar riel de corredera de cajón",
            "Rieles telescópicos de balines • Deslizamiento suave",
            "Sustituye correderas vencidas de gavetas o cajones de clóset que se salen de su guía.",
            "green", "Reparación sencilla",
            "Montaje con tornillos cortos para madera usando destornillador de mano.",
            "Fácil", "~40 min", 26000, "Par de rieles telescópicos 40cm",
            "1 cajón", "1 juego", "Inmediato", "~65%",
            "Marca con lápiz la línea guía en el mueble usando escuadra para que el cajón no entre torcido.",
            "Cajón que abre al 100% con deslizamiento silencioso y soporte de peso firme.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCEsLDHiCC2pQBGdntWJa5ePKOOAeppP1EDpxsAw2cL-R2uZktrA41ido2kmWfsSNTB57EL8k6QlOokM_isrZzn5wej7LfRG1fg36RF4mj9ai2A02J7Jwo2ULVJfp7bhOSfUTy5cBL6sc2V-ciHhdhNOxoPCk4SwppHOcCRs_6SeAJ1WGGDoPXPg_FvnrImDltH1MF-UOywZ0ufIiP6mh-zHmBTvy7xyk3-7b7opBEG28t179_xIboM",
            0, 0
        ),

        # --- CAT 7: BAÑO Y COCINA ---
        (
            "task_renovar_silicona", "cat_bano_cocina", "Sellar ducha o lavamanos con silicona",
            "Silicona antihongos • Calafateo limpio",
            "Retira el sellador ennegrecido y aplica un nuevo cordón impermeable resistente al moho.",
            "green", "Reparación sencilla",
            "Tarea estética de impermeabilización superficial con ventilación estándar.",
            "Fácil", "~1 hora", 24000, "Silicona acética con fungicida",
            "Tubo de 280 ml", "1 cordón perimetral", "24 hrs secado", "~70%",
            "Limpia la superficie con alcohol y sécala por completo antes de aplicar el nuevo cordón.",
            "Junta limpia, brillante y 100% impermeable que previene filtraciones y moho.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCEsLDHiCC2pQBGdntWJa5ePKOOAeppP1EDpxsAw2cL-R2uZktrA41ido2kmWfsSNTB57EL8k6QlOokM_isrZzn5wej7LfRG1fg36RF4mj9ai2A02J7Jwo2ULVJfp7bhOSfUTy5cBL6sc2V-ciHhdhNOxoPCk4SwppHOcCRs_6SeAJ1WGGDoPXPg_FvnrImDltH1MF-UOywZ0ufIiP6mh-zHmBTvy7xyk3-7b7opBEG28t179_xIboM",
            0, 1
        ),
        (
            "task_descalcificar_ducha", "cat_bano_cocina", "Descalcificar regadera y aireadores",
            "Vinagre blanco • Limpieza de sarro mineral",
            "Elimina el taponamiento por sarro que desvía los chorros de la ducha o reduce la presión.",
            "green", "Reparación sencilla",
            "Solución biodegradable casera sin riesgo corrosivo.",
            "Muy fácil", "~20 min + remojo", 9000, "Vinagre blanco y cepillo suave",
            "1 regadera + 2 grifos", "1 desincrustación", "4 hrs remojo", "~95%",
            "Sujeta una bolsa plástica con vinagre a la regadera con una banda elástica para no tener que desmontarla.",
            "Chorros paralelos, homogéneos y con máxima presión de salida.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuBsmIvtuPilapbZVRiuZiLFOlz4J4dvLlD0gfE4QnlMDJ7wEIrNrZBWJ-FsK76I3Ii-L1LG_F-bD3JKHEifrVYmfJInwifGvQZyGvQ1Ti6LpPt5CrbBYAJRdAirxh9iuPu-s_NVoM906ycICln6Sep3eRFy_uGkAQEvJ1BAeQQy3LCwshzwMs_fqHsSYfyvCFiai0hRLkzB7Pw8hKEnxY6bBuSUICBrNa5oHXjlghb3IgH_6nnMSYdp",
            0, 0
        ),
        (
            "task_cambiar_herraje_sanitario", "cat_bano_cocina", "Cambiar válvula de descarga del sanitario",
            "Torre de llenado regulable • Sapo de silicona",
            "Soluciona el paso continuo de agua en el tanque del inodoro cambiando la válvula interior.",
            "green", "Reparación sencilla",
            "Trabajo dentro del tanque con la llave de paso del inodoro cerrada.",
            "Fácil", "~40 min", 35000, "Kit universal de herrajes sanitario",
            "1 sanitario", "1 cambio completo", "Inmediato", "~70%",
            "Gradúa el flotador para que el nivel de agua quede 2 cm por debajo del tubo de rebose.",
            "Corte exacto de agua al llenar y cero desperdicio silencioso en la taza.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuB5D5oVmAmuZT4voN3AarMdeplN5m6eUfuh1DNohm0t-BG6cuQFHGdZkoEEcori0H5EOv_QRjE3Yelwop-DEpFvUuBJ6h3ETHh6Zz3yZkqGJrltwsqY6L2TIQthcQeXG7OYTBcGy3m35oLaM_v3Z2xoeoSvs-k2c2zy1ilYkD6c2HDMLgFYSwsDFE45BfbZsjfPD1wh-o0yISIA59W1uqZztVyU3OHfpX6yoVZwdDbECdFYACobdwhi",
            0, 0
        ),

        # --- CAT 8: MANTENIMIENTO PREVENTIVO ---
        (
            "task_limpiar_filtros_campana", "cat_mantenimiento", "Limpieza de filtros de campana extractora",
            "Desengrase de mallas metálicas • Agua tibia",
            "Devuelve la capacidad de succión a la campana eliminando grasa acumulada.",
            "green", "Reparación sencilla",
            "Limpieza preventiva con productos caseros sin desmontajes complejos.",
            "Muy fácil", "~30 min", 10000, "Desengrasante multiusos y bicarbonato",
            "2 a 3 rejillas", "1 lavado", "Inmediato", "~90%",
            "Remoja los filtros en agua caliente con bicarbonato y jabón líquido durante 20 minutos.",
            "Filtros plateados y destapados con flujo de aire óptimo.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuB5D5oVmAmuZT4voN3AarMdeplN5m6eUfuh1DNohm0t-BG6cuQFHGdZkoEEcori0H5EOv_QRjE3Yelwop-DEpFvUuBJ6h3ETHh6Zz3yZkqGJrltwsqY6L2TIQthcQeXG7OYTBcGy3m35oLaM_v3Z2xoeoSvs-k2c2zy1ilYkD6c2HDMLgFYSwsDFE45BfbZsjfPD1wh-o0yISIA59W1uqZztVyU3OHfpX6yoVZwdDbECdFYACobdwhi",
            0, 0
        ),
        (
            "task_revisar_humedades", "cat_mantenimiento", "Tratamiento de mancha de humedad superficial",
            "Impermeabilizante base solvente • Bloqueador",
            "Detén el avance de eflorescencias y manchas amarillentas en techos o muros secos.",
            "yellow", "Precaución requerida",
            "Requiere verificar primero que la filtración origen ya fue reparada y que el muro esté seco.",
            "Intermedia", "~1.5 h", 29000, "Pintura bloqueadora de manchas",
            "~4 m²", "2 capas", "3 hrs", "~65%",
            "Nunca pintes sobre un muro húmedo o con moho vivo; límpialo primero con agua clorada y déjalo secar.",
            "Superficie blanca sellada que no deja reaparecer la aureola amarilla.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuDkGFETcHQ3pfGR2EJTTRntA0g0QNXshRyMmOPh9zcNomqvrVm6ZiONoetRBO9MofXbkyjGhZqK3nYKueRz_N1Ti6mXCegllLmOYnq-LfIsYJLuTQpdNOqoMtBUaL834t1Dz5aztrRYxVeCq_MPRYsYqCvqQDmNIMQ6RqrmrYVvWrkq0_5m_GHZ4RR94gDmVCtTcm_BIAw5DHEV9JjkFNE84g6OluagACeesPO63mY4jVfMZT_T_rD6",
            0, 0
        ),
        (
            "task_gas_calentador_rojo", "cat_mantenimiento", "Mantenimiento o fuga en calentador de gas",
            "Red de gas combustible • Válvulas y quemador",
            "Intervención de calentadores de paso, estufas o tuberías de gas domiciliario.",
            "red", "Requiere un profesional",
            "RIESGO MORTAL DE INTOXICACIÓN POR MONÓXIDO DE CARBONO (CO), DEFLAGRACIÓN O EXPLOSIÓN.",
            "Especializada", "N/A", 0, "Certificación técnica de gas",
            "N/A", "N/A", "N/A", "0%",
            "Si percibe olor a gas: NO encienda interruptores ni fuego, abra ventanas, cierre la llave de paso y evacúe.",
            "Servicio exclusivo de técnicos certificados por la empresa distribuidora de gas.",
            "https://lh3.googleusercontent.com/aida-public/AB6AXuCEsLDHiCC2pQBGdntWJa5ePKOOAeppP1EDpxsAw2cL-R2uZktrA41ido2kmWfsSNTB57EL8k6QlOokM_isrZzn5wej7LfRG1fg36RF4mj9ai2A02J7Jwo2ULVJfp7bhOSfUTy5cBL6sc2V-ciHhdhNOxoPCk4SwppHOcCRs_6SeAJ1WGGDoPXPg_FvnrImDltH1MF-UOywZ0ufIiP6mh-zHmBTvy7xyk3-7b7opBEG28t179_xIboM",
            1, 0
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

    # 4. Insumos Desglosados en Gamas (Base, Eco, Recom, Prem)
    materials = [
        # --- PINTAR PARED ---
        ("task_pintar_pared", "base", "Pintura Tipo 1 acrílica lavable", "Galón blanco de primera calidad", 82000, "palette", 1),
        ("task_pintar_pared", "base", "Masilla para estuco interior", "Tubo de 250g para resanes", 8500, "construction", 1),
        ("task_pintar_pared", "base", "Lija suave al agua grano 180", "Pliego para desbaste fino", 2000, "texture", 1),
        ("task_pintar_pared", "base", "Plástico protector de piso (2x3m)", "Película de polietileno calibre 2", 4000, "layers", 1),
        ("task_pintar_pared", "eco", "Galón de vinilo estándar Tipo 2", "1 galón / 3.78 L • Rendimiento 20-25 m²", 58000, "check_circle", 1),
        ("task_pintar_pared", "eco", "Rodillo básico de felpa sintética", "Rodillo 9 pulgadas para uso doméstico", 15000, "check_circle", 1),
        ("task_pintar_pared", "eco", "Cinta de enmascarar estándar 18mm", "Adhesivo suave para zócalos", 5000, "check_circle", 1),
        ("task_pintar_pared", "eco", "Tubo estuco acrílico pequeño 200g", "Para tapar pequeñas grietas", 8000, "check_circle", 1),
        ("task_pintar_pared", "eco", "Pliego de plástico protector delgado", "Protección ligera para piso", 12000, "check_circle", 1),
        ("task_pintar_pared", "recom", "Galón de vinilo acrílico Tipo 1", "1 galón / 3.78 L • Rendimiento 25-30 m²", 82000, "colors", 1),
        ("task_pintar_pared", "recom", "Rodillo felpa 9\" antigota + bandeja", "Mango ergonómico con rosca para extensión", 24500, "brush", 1),
        ("task_pintar_pared", "recom", "Brocha cerda angular suave 2.5\"", "Corte perfecto de esquinas y marcos", 14000, "brush", 1),
        ("task_pintar_pared", "recom", "Cinta pintor azul resistente UV 24mm", "No deja residuos de pegante ni levanta pintura", 12000, "line_weight", 1),
        ("task_pintar_pared", "recom", "Masilla estuco interior 450g + espátula", "Masilla lista para usar y lija suave #180", 16000, "handyman", 1),
        ("task_pintar_pared", "prem", "Galón esmalte al agua antibacterial", "1 galón • Máxima lavabilidad y protección anti-hongos", 128000, "check_circle", 1),
        ("task_pintar_pared", "prem", "Kit rodillo microfibra pro + extensión 1.2m", "Acabado ultra sedoso sin salpicaduras", 38000, "check_circle", 1),
        ("task_pintar_pared", "prem", "Cinta precisión bordes nítidos 24mm", "Tecnología Bloqueador de Pintura (PaintBlock)", 19000, "check_circle", 1),
        ("task_pintar_pared", "prem", "Pasta resanadora ultra-rápida + espátula inox", "Acabado espejo en 15 minutos", 18000, "check_circle", 1),
        ("task_pintar_pared", "prem", "Manta textil absorbente plastificada 4x4m", "Reutilizable y anti-deslizante", 12000, "check_circle", 1),

        # --- RETOCAR ZÓCALOS ---
        ("task_retocar_zocalos", "base", "Esmalte al agua blanco zócalos (1/4 gal)", "Acabado semibrillante lavable", 18000, "palette", 1),
        ("task_retocar_zocalos", "base", "Brocha para zócalo 1.5\"", "Cerdas finas para trazo recto", 4500, "brush", 1),
        ("task_retocar_zocalos", "base", "Cinta de papel 18mm", "Protección de borde de piso", 2500, "line_weight", 1),
        ("task_retocar_zocalos", "eco", "Cuarto de vinilo estándar", "Rendimiento 10 m lineales", 14000, "check_circle", 1),
        ("task_retocar_zocalos", "eco", "Brocha estándar 1 pulgada", "Brocha económica", 3500, "check_circle", 1),
        ("task_retocar_zocalos", "recom", "Cuarto de esmalte base agua", "Lavable y de secado rápido", 18000, "check_circle", 1),
        ("task_retocar_zocalos", "recom", "Brocha cerda suave 1.5\" + cinta azul", "Acabado limpio sin marcas", 7000, "check_circle", 1),
        ("task_retocar_zocalos", "prem", "Esmalte poliuretano de alto tráfico", "Resistente a patadas y trapero", 28000, "check_circle", 1),
        ("task_retocar_zocalos", "prem", "Pincel de recorte profesional cerda dorada", "Precisión milimétrica", 11000, "check_circle", 1),

        # --- PINTAR PUERTA ---
        ("task_pintar_puerta", "base", "Esmalte sintético brillante (1/4 gal)", "Protección para madera interior", 24000, "palette", 1),
        ("task_pintar_puerta", "base", "Mini rodillo de espuma para esmaltes", "Sin burbujas ni textura", 8500, "brush", 1),
        ("task_pintar_puerta", "base", "Lija para madera grano 150", "Preparación previa", 2000, "texture", 1),
        ("task_pintar_puerta", "eco", "Pintura base aceite convencional", "Color estándar blanco o caoba", 19000, "check_circle", 1),
        ("task_pintar_puerta", "eco", "Brocha cerda negra 2\"", "Uso general", 6000, "check_circle", 1),
        ("task_pintar_puerta", "recom", "Esmalte al agua secado rápido", "Sin olor penetrante a solvente", 27000, "check_circle", 1),
        ("task_pintar_puerta", "recom", "Mini rodillo espuma alta densidad + lija", "Acabado liso uniforme", 11000, "check_circle", 1),
        ("task_pintar_puerta", "prem", "Laca poliuretano de alta dureza", "Resistencia superior a rayones", 42000, "check_circle", 1),
        ("task_pintar_puerta", "prem", "Rodillo flockater microfibra fino", "Aspecto lacado de fábrica", 16000, "check_circle", 1),

        # --- TAPAR HUECOS ---
        ("task_resanar_agujeros", "base", "Estuco plástico interior en tubo 250g", "Masilla blanca lista para aplicar", 8500, "construction", 1),
        ("task_resanar_agujeros", "base", "Lija al agua grano fino #220", "Pliego para acabado suave al tacto", 2000, "texture", 1),
        ("task_resanar_agujeros", "base", "Espátula plástica flexible 2\"", "Ideal para no rayar la pared", 5500, "handyman", 1),
        ("task_resanar_agujeros", "eco", "Estuco acrílico pote económico 200g", "Relleno para 10 huecos", 6000, "check_circle", 1),
        ("task_resanar_agujeros", "eco", "Espátula plástica básica y lija", "Kit básico de resane", 5500, "check_circle", 1),
        ("task_resanar_agujeros", "recom", "Tubo estuco plástico dosificador 250g", "Aplicación limpia sin desperdicio", 9500, "check_circle", 1),
        ("task_resanar_agujeros", "recom", "Espátula metálica flexible 2\" + lija #220", "Acabado al ras impecable", 8500, "check_circle", 1),
        ("task_resanar_agujeros", "prem", "Pasta resanadora ultra-ligera en pote", "No encoge ni se agrieta al secar", 18000, "check_circle", 1),
        ("task_resanar_agujeros", "prem", "Espátula de acero inoxidable ergonómica", "Máxima durabilidad y precisión", 14000, "check_circle", 1),

        # --- REPARAR FISURA SUPERFICIAL ---
        ("task_reparar_grieta_superficial", "base", "Masilla elastomérica antifisuras 500g", "Sella y absorbe dilataciones", 18000, "construction", 1),
        ("task_reparar_grieta_superficial", "base", "Cinta de malla de fibra de vidrio 5cmx10m", "Puente de unión resistente", 9500, "texture", 1),
        ("task_reparar_grieta_superficial", "base", "Espátula de 3 pulgadas", "Aplicación uniforme de masilla", 4500, "handyman", 1),
        ("task_reparar_grieta_superficial", "eco", "Masilla para juntas estándar", "Relleno básico de fisuras", 12000, "check_circle", 1),
        ("task_reparar_grieta_superficial", "eco", "Cinta de papel microperforada", "Refuerzo para grietas menores", 6000, "check_circle", 1),
        ("task_reparar_grieta_superficial", "recom", "Masilla elastomérica flexible 500g", "Garantía de no reapertura", 18000, "check_circle", 1),
        ("task_reparar_grieta_superficial", "recom", "Cinta autoadhesiva de malla de fibra 10m", "Fijación instantánea sin arrugas", 9500, "check_circle", 1),
        ("task_reparar_grieta_superficial", "recom", "Lija grano 150 y espátula", "Acabado parejo con el muro", 4500, "check_circle", 1),
        ("task_reparar_grieta_superficial", "prem", "Sellador híbrido polímero MS + masilla pro", "Máxima elasticidad permanente", 32000, "check_circle", 1),
        ("task_reparar_grieta_superficial", "prem", "Malla de fibra bidireccional de alto módulo", "Para micro-fisuras recurrentes", 14000, "check_circle", 1),

        # --- FIJAR ESQUINERO DRYWALL ---
        ("task_fijar_esquinero_drywall", "base", "Esquinero metálico perforado 2.4m", "Perfil galvanizado de esquina", 9000, "construction", 1),
        ("task_fijar_esquinero_drywall", "base", "Masilla para drywall 1 kg", "Compuesto para juntas", 11000, "palette", 1),
        ("task_fijar_esquinero_drywall", "base", "Tornillos cabeza de lenteja 1/2\"", "Fijación al parante de acero", 3500, "build", 1),
        ("task_fijar_esquinero_drywall", "eco", "Esquinero de PVC económico y masilla básica", "Reparación puntual de esquina", 16000, "check_circle", 1),
        ("task_fijar_esquinero_drywall", "recom", "Esquinero metálico galvanizado + masilla lista", "Rigidez y resistencia a impactos", 23500, "check_circle", 1),
        ("task_fijar_esquinero_drywall", "prem", "Esquinero cinta armada papel-metal pro", "Acabado perfecto de fábrica", 36000, "check_circle", 1),

        # --- INSTALAR REPISA ---
        ("task_instalar_repisa", "base", "Soportes invisibles de acero (par)", "Varillas empotradas para madera", 26000, "build", 1),
        ("task_instalar_repisa", "base", "Chazos de expansión 5/16\" con tornillos", "Juego de 4 anclajes seguros", 4500, "construction", 1),
        ("task_instalar_repisa", "base", "Broca para mampostería 5/16\" punta tungsteno", "Perforación precisa en ladrillo", 7500, "build", 1),
        ("task_instalar_repisa", "eco", "Escuadras metálicas visibles simples (par)", "Soporte de ángulo estándar", 12000, "check_circle", 1),
        ("task_instalar_repisa", "eco", "Chazos plásticos 1/4\" con tornillos (x4)", "Fijación liviana", 3500, "check_circle", 1),
        ("task_instalar_repisa", "recom", "Soportes invisibles reforzados (par)", "Estética limpia y oculta", 26000, "check_circle", 1),
        ("task_instalar_repisa", "recom", "Chazos de expansión 5/16\" + broca widia", "Anclaje firme hasta 15 kg", 12000, "check_circle", 1),
        ("task_instalar_repisa", "prem", "Herraje flotante industrial de placa corrida", "Carga pesada hasta 30 kg", 44000, "check_circle", 1),
        ("task_instalar_repisa", "prem", "Chazos metálicos Fisher SX Plus + broca Bosch", "Máxima seguridad estructural", 18000, "check_circle", 1),

        # --- COLGAR CUADROS ---
        ("task_colgar_cuadros", "base", "Kit de anclajes para cuadros surtidos", "Ganchos de 1 y 2 clavos de acero", 8500, "build", 1),
        ("task_colgar_cuadros", "base", "Cáncamos y alambre trenzado 3m", "Para bastidores de madera", 3500, "hardware", 1),
        ("task_colgar_cuadros", "eco", "Clavos acerados con cabeza de bronce", "Para 4 cuadros pequeños", 5000, "check_circle", 1),
        ("task_colgar_cuadros", "recom", "Ganchos autoperforantes y alambre galvanizado", "Sujeción segura hasta 8 kg", 12000, "check_circle", 1),
        ("task_colgar_cuadros", "prem", "Tiras adhesivas de soporte Command 3M", "Sin agujeros ni marcas al retirar", 22000, "check_circle", 1),

        # --- INSTALAR CORTINERO ---
        ("task_instalar_cortinero", "base", "Soportes de pared dobles para tubo 1\"", "Par de soportes con acabado niquelado", 18000, "build", 1),
        ("task_instalar_cortinero", "base", "Chazos mariposa para drywall / expansión", "Fijación firme en dintel", 6500, "construction", 1),
        ("task_instalar_cortinero", "base", "Terminales decorativos para barra (par)", "Cierre de tubo estético", 9500, "star", 1),
        ("task_instalar_cortinero", "eco", "Soportes sencillos de aluminio y tornillos", "Para visillo liviano", 14000, "check_circle", 1),
        ("task_instalar_cortinero", "recom", "Soportes dobles reforzados + chazos de carga", "Para blackout y cortina pesada", 26000, "check_circle", 1),
        ("task_instalar_cortinero", "prem", "Riel europeo de deslizamiento silencioso", "Acabado hotelero de lujo", 52000, "check_circle", 1),

        # --- CAMBIAR BOMBILLO / PLAFÓN ---
        ("task_cambiar_bombillo", "base", "Plafón / roseta de porcelana E27", "Aislante térmico de alta seguridad", 6500, "lightbulb", 1),
        ("task_cambiar_bombillo", "base", "Bombillo LED luz cálida 9W (equiv 60W)", "Ahorro energético 85%", 8500, "wb_incandescent", 1),
        ("task_cambiar_bombillo", "eco", "Plafón plástico estándar + bombillo LED 7W", "Iluminación básica", 10000, "check_circle", 1),
        ("task_cambiar_bombillo", "recom", "Plafón porcelana reforzada + LED Philips 9W", "Larga vida útil 15.000 hrs", 15000, "check_circle", 1),
        ("task_cambiar_bombillo", "prem", "Plafón decorativo metálico + bombillo dimerizable", "Confort visual y diseño", 32000, "check_circle", 1),

        # --- CAMBIAR INTERRUPTOR ---
        ("task_cambiar_interruptor", "base", "Interruptor sencillo unipolar 10A blanco", "Placa con balancín suave", 12500, "toggle_on", 1),
        ("task_cambiar_interruptor", "base", "Cinta aislante eléctrica de PVC negra", "Retardante de llama 600V", 4500, "tape", 1),
        ("task_cambiar_interruptor", "base", "Tornillos de sujeción a caja 5800", "Fijación milimétrica", 2000, "build", 1),
        ("task_cambiar_interruptor", "eco", "Interruptor línea estándar residencial", "Certificación básica RETIE", 11000, "check_circle", 1),
        ("task_cambiar_interruptor", "recom", "Interruptor placa modular de alta gama (ej. Legrand/Bticino)", "Acabado mate resistente a rayas", 22000, "check_circle", 1),
        ("task_cambiar_interruptor", "prem", "Interruptor con luz piloto nocturna o táctil", "Diseño contemporáneo de lujo", 38000, "check_circle", 1),

        # --- CAMBIAR EMPAQUE GRIFO ---
        ("task_cambiar_empaque_grifo", "base", "Juego de cueritos y empaques surtidos nitrilo", "Resistentes al agua caliente y fría", 4500, "valve", 1),
        ("task_cambiar_empaque_grifo", "base", "Cinta de teflón para fontanería 1/2\"", "Sellado de roscas antifugas", 3000, "texture", 1),
        ("task_cambiar_empaque_grifo", "eco", "Empaques planos estándar de caucho", "Para grifo convencional", 4000, "check_circle", 1),
        ("task_cambiar_empaque_grifo", "recom", "Empaques cónicos de silicona + teflón pro", "Sellado hermético de larga duración", 9500, "check_circle", 1),
        ("task_cambiar_empaque_grifo", "prem", "Cartucho de disco cerámico de 1/4 de giro", "Reemplazo completo de núcleo", 24000, "check_circle", 1),

        # --- LIMPIAR SIFÓN ---
        ("task_limpiar_sifon", "base", "Juego de empaques cónicos para sifón 1-1/4\"", "Sellado entre tubos plásticos", 4500, "water_drop", 1),
        ("task_limpiar_sifon", "base", "Cinta de teflón y cepillo limpiador", "Para remoción de sedimentos", 5000, "cleaning_services", 1),
        ("task_limpiar_sifon", "eco", "Empaques de goma planos universales", "Mantenimiento básico de fuga", 5500, "check_circle", 1),
        ("task_limpiar_sifon", "recom", "Sifón flexible en acordeón PVC nuevo", "Reemplazo total libre de atascos", 16000, "check_circle", 1),
        ("task_limpiar_sifon", "prem", "Sifón rígido metálico cromado de lujo", "Estética visible para muebles abiertos", 42000, "check_circle", 1),

        # --- AJUSTAR BISAGRA MUEBLE ---
        ("task_ajustar_bisagra", "base", "Tornillos cabeza avellanada para aglomerado 3.5x15mm", "Fijación firme en orificios barridos", 3000, "build", 1),
        ("task_ajustar_bisagra", "base", "Topes de silicona para amortiguar golpe", "Cierre silencioso de puertas", 2500, "volume_off", 1),
        ("task_ajustar_bisagra", "eco", "Tornillos para madera estándar y tarugos", "Calibración simple", 4500, "check_circle", 1),
        ("task_ajustar_bisagra", "recom", "Tornillos reforzados y bisagra parche estándar de repuesto", "Solución definitiva", 8000, "check_circle", 1),
        ("task_ajustar_bisagra", "prem", "Bisagra cierre lento amortiguada (soft-close)", "Cierre suave automático", 19000, "check_circle", 1),

        # --- LUBRICAR CERRADURA ---
        ("task_lubricar_cerradura", "base", "Tubo de grafito puro micro-pulverizado", "Lubricante seco especial para cilindros", 9500, "key", 1),
        ("task_lubricar_cerradura", "base", "Trapo de microfibra desengrasante", "Limpieza de pestillo y llave", 3000, "cleaning_services", 1),
        ("task_lubricar_cerradura", "eco", "Aceite fino de máquina multiusos", "Lubricación superficial básica", 6000, "check_circle", 1),
        ("task_lubricar_cerradura", "recom", "Grafito en polvo para cerraduras 50g", "Sin atrapar mugre ni apelmazar", 14000, "check_circle", 1),
        ("task_lubricar_cerradura", "prem", "Lubricante sintético con PTFE de secado rápido", "Protección anticorrosiva extrema", 26000, "check_circle", 1),

        # --- CORREDERA DE CAJÓN ---
        ("task_reparar_corredera_cajon", "base", "Par de rieles telescópicos 40cm con balines", "Soporta hasta 25 kg de carga", 18500, "table_rows", 1),
        ("task_reparar_corredera_cajon", "base", "Tornillos para riel de madera 3x12mm", "Fijación precisa a ras", 3500, "build", 1),
        ("task_reparar_corredera_cajon", "eco", "Rieles simples de rueda de nylon blancos", "Apertura 3/4 básica", 12000, "check_circle", 1),
        ("task_reparar_corredera_cajon", "recom", "Rieles telescópicos extensión total 40cm", "Acceso cómodo a todo el cajón", 26000, "check_circle", 1),
        ("task_reparar_corredera_cajon", "prem", "Rieles telescópicos con cierre suave (soft-close)", "Antigolpes con freno integrado", 46000, "check_circle", 1),

        # --- RENOVAR SILICONA ---
        ("task_renovar_silicona", "base", "Tubo de silicona acética antihongos blanca 280ml", "Protección contra moho por 5 años", 18000, "shower", 1),
        ("task_renovar_silicona", "base", "Cinta de enmascarar para delimitar bordes", "Para cordón recto y estético", 4500, "line_weight", 1),
        ("task_renovar_silicona", "eco", "Silicona multiusos tubo pequeño 85ml", "Reparación puntual de esquina", 11000, "check_circle", 1),
        ("task_renovar_silicona", "recom", "Silicona cartucho 280ml con fungicida + cinta", "Sellado profesional de ducha", 24000, "check_circle", 1),
        ("task_renovar_silicona", "prem", "Polímero sellador híbrido anti-manchas 10 años", "Pintable y de máxima resistencia química", 39000, "check_circle", 1),

        # --- DESCALCIFICAR DUCHA ---
        ("task_descalcificar_ducha", "base", "Botella de vinagre blanco concentrado 1L", "Ácido acético natural desincrustante", 4500, "sanitizer", 1),
        ("task_descalcificar_ducha", "base", "Cepillo de cerdas de nylon finas", "Limpieza de toberas de goma", 3500, "brush", 1),
        ("task_descalcificar_ducha", "eco", "Vinagre casero y bolsa de inmersión", "Tratamiento clásico casero", 5000, "check_circle", 1),
        ("task_descalcificar_ducha", "recom", "Vinagre concentrado + cepillo de precisión", "Limpieza profunda de chorro", 9000, "check_circle", 1),
        ("task_descalcificar_ducha", "prem", "Desincrustante antical profesional + aireadores nuevos", "Rendimiento como nuevo", 24000, "check_circle", 1),

        # --- CAMBIAR HERRAJE SANITARIO ---
        ("task_cambiar_herraje_sanitario", "base", "Válvula de entrada de agua tipo flotador regulable", "Corte hidráulico preciso", 19000, "plumbing", 1),
        ("task_cambiar_herraje_sanitario", "base", "Sapo / obturador de silicona resistente a cloro", "Sello de descarga sin fugas", 8500, "water_drop", 1),
        ("task_cambiar_herraje_sanitario", "eco", "Sapo de caucho estándar de reemplazo", "Solución rápida de goteo", 8000, "check_circle", 1),
        ("task_cambiar_herraje_sanitario", "recom", "Kit universal de torre de llenado y sapo de silicona", "Ajuste para cualquier sanitario", 35000, "check_circle", 1),
        ("task_cambiar_herraje_sanitario", "prem", "Sistema de descarga dual (ahorro agua 3/6L)", "Ahorro del 50% de agua mensual", 58000, "check_circle", 1),

        # --- LIMPIAR FILTROS CAMPANA ---
        ("task_limpiar_filtros_campana", "base", "Desengrasante doméstico concentrado 500ml", "Acción rápida sobre grasas de cocina", 7500, "soap", 1),
        ("task_limpiar_filtros_campana", "base", "Bicarbonato de sodio puro 250g", "Potenciador natural de lavado", 2500, "cleaning_services", 1),
        ("task_limpiar_filtros_campana", "eco", "Jabón lavaplatos desengrasante + agua caliente", "Limpieza básica rutinaria", 6000, "check_circle", 1),
        ("task_limpiar_filtros_campana", "recom", "Desengrasante industrial cítrico + bicarbonato", "Desincrustación total de mallas", 10000, "check_circle", 1),
        ("task_limpiar_filtros_campana", "prem", "Filtros de carbón activado nuevos para reposición", "Máxima purificación de olores", 34000, "check_circle", 1),

        # --- REVISAR HUMEDADES ---
        ("task_revisar_humedades", "base", "Pintura bloqueadora de manchas al solvente (1/4 gal)", "Sello impermeable contra aureolas", 22000, "format_paint", 1),
        ("task_revisar_humedades", "base", "Solución fungicida lavable", "Desinfección de esporas de moho", 5500, "sanitizer", 1),
        ("task_revisar_humedades", "eco", "Solución de cloro y sellador acrílico", "Tratamiento superficial básico", 14000, "check_circle", 1),
        ("task_revisar_humedades", "recom", "Bloqueador antimanchas + fungicida líquido", "Previene rebrote de aureola", 29000, "check_circle", 1),
        ("task_revisar_humedades", "prem", "Impermeabilizante nanotecnológico + pintura térmica", "Aislamiento contra condensación", 54000, "check_circle", 1)
    ]

    cursor.execute("DELETE FROM task_materials")
    for mat in materials:
        cursor.execute("""
            INSERT INTO task_materials (task_id, tier, name, description, unit_price_cop, icon, is_essential)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, mat)

    # 5. Herramientas Requeridas por Tarea
    tools = [
        ("task_pintar_pared", "Rodillo con felpa antigoteo 9\"", "brush", 0),
        ("task_pintar_pared", "Brocha 2.5\" corte angular", "brush", 0),
        ("task_pintar_pared", "Bandeja plástica reforzada", "format_paint", 0),
        ("task_pintar_pared", "Espátula metálica de 2\"", "handyman", 1),
        ("task_pintar_pared", "Cinta de enmascarar azul", "line_weight", 1),
        ("task_retocar_zocalos", "Brocha fina para zócalos 1.5\"", "brush", 1),
        ("task_retocar_zocalos", "Trapo de algodón limpio", "cleaning_services", 1),
        ("task_pintar_puerta", "Mini rodillo de espuma 4\"", "brush", 0),
        ("task_pintar_puerta", "Cuñas de madera para piso", "hardware", 1),
        ("task_resanar_agujeros", "Espátula flexible de 2\" o 3\"", "handyman", 1),
        ("task_resanar_agujeros", "Trapo húmedo limpio", "cleaning_services", 1),
        ("task_reparar_grieta_superficial", "Espátula ancha de 4\" o 6\"", "handyman", 1),
        ("task_reparar_grieta_superficial", "Bisturí para sanear la grieta", "content_cut", 1),
        ("task_fijar_esquinero_drywall", "Tijeras para hojalata / cortar metal", "content_cut", 0),
        ("task_fijar_esquinero_drywall", "Espátula de esquina o llana plana", "handyman", 1),
        ("task_instalar_repisa", "Taladro con percutor", "build", 0),
        ("task_instalar_repisa", "Nivel de burbuja", "square_foot", 1),
        ("task_instalar_repisa", "Cinta métrica y lápiz", "straighten", 1),
        ("task_colgar_cuadros", "Martillo de uña pequeño", "hardware", 1),
        ("task_colgar_cuadros", "Nivel de burbuja compacto", "square_foot", 1),
        ("task_instalar_cortinero", "Taladro percutor con broca 5/16\"", "build", 0),
        ("task_instalar_cortinero", "Escalera de tijera de 3 pasos", "stairs", 1),
        ("task_instalar_cortinero", "Nivel largo de mano", "square_foot", 1),
        ("task_cambiar_bombillo", "Escalera de tijera firme", "stairs", 1),
        ("task_cambiar_bombillo", "Destornillador con mango aislado", "handyman", 1),
        ("task_cambiar_interruptor", "Buscapolo o probador de tensión", "electric_meter", 0),
        ("task_cambiar_interruptor", "Destornillador de estrella #1", "handyman", 1),
        ("task_cambiar_interruptor", "Pinza pelacables o alicate plano", "handyman", 1),
        ("task_cambiar_empaque_grifo", "Llave expansiva o ajustable de 8\"", "build", 1),
        ("task_cambiar_empaque_grifo", "Destornillador plano fino", "handyman", 1),
        ("task_limpiar_sifon", "Balde plástico mediano", "delete", 1),
        ("task_limpiar_sifon", "Guantes de caucho de cocina", "front_hand", 1),
        ("task_ajustar_bisagra", "Destornillador de estrella #2", "handyman", 1),
        ("task_lubricar_cerradura", "Paño suave de limpieza", "cleaning_services", 1),
        ("task_reparar_corredera_cajon", "Destornillador de estrella", "handyman", 1),
        ("task_reparar_corredera_cajon", "Regla de metal o escuadra", "square_foot", 1),
        ("task_renovar_silicona", "Pistola para silicona de calafateo", "shower", 0),
        ("task_renovar_silicona", "Bisturí o cuchilla para silicona vieja", "content_cut", 1),
        ("task_descalcificar_ducha", "Bolsa plástica con cierre hermético", "inventory_2", 1),
        ("task_descalcificar_ducha", "Banda elástica o cinta adhesiva", "line_weight", 1),
        ("task_cambiar_herraje_sanitario", "Llave expansiva o alicate de presión", "build", 1),
        ("task_cambiar_herraje_sanitario", "Esponja absorbente para el fondo", "cleaning_services", 1),
        ("task_limpiar_filtros_campana", "Recipiente hondo o platón", "inventory_2", 1),
        ("task_limpiar_filtros_campana", "Cepillo de cerdas suaves", "brush", 1),
        ("task_revisar_humedades", "Brocha de 3\" cerda dura", "brush", 1),
        ("task_revisar_humedades", "Guantes y gafas protectoras", "visibility", 1)
    ]

    cursor.execute("DELETE FROM task_tools")
    for tool in tools:
        cursor.execute("""
            INSERT INTO task_tools (task_id, name, icon, is_common)
            VALUES (?, ?, ?, ?)
        """, tool)

    # 6. Pasos Guía Detallados para Todas las Tareas Autónomas
    steps = [
        # --- PINTAR PARED ---
        ("task_pintar_pared", 1, "Despeje y protección del área", "Retira muebles hacia el centro del cuarto, quita cuadros y tapas plásticas de tomas eléctricas. Cubre el piso con plástico y fija zócalos con cinta de enmascarar.", "Asegúrate de que el plástico no resbale al caminar calzado."),
        ("task_pintar_pared", 2, "Resane y lijado previo", "Aplica estuco en orificios o raspaduras con la espátula. Deja secar 45 min y lija suavemente con grano #180.", "Pasa un paño seco para eliminar el polvo antes de comenzar a pintar."),
        ("task_pintar_pared", 3, "Recorte perimetral de bordes", "Con la brocha angular de 2.5\", pinta una franja de 5 cm a lo largo del techo, zócalos, esquinas y alrededor de tomas.", "Mantén la brocha húmeda con suficiente pintura sin que gotee."),
        ("task_pintar_pared", 4, "Primera mano uniforme con rodillo", "Carga el rodillo en la bandeja escurriendo el exceso. Aplica en la pared dibujando una 'W' o 'M' para distribuir parejo.", "Trabaja por secciones de 1 metro cuadrado sin presionar con fuerza."),
        ("task_pintar_pared", 5, "Segunda mano y acabado final", "Espera de 2 a 3 horas de secado y aplica la segunda mano uniforme en pasadas verticales continuas.", "Retira la cinta de enmascarar mientras la pintura aún esté ligeramente fresca."),

        # --- RETOCAR ZÓCALOS ---
        ("task_retocar_zocalos", 1, "Limpieza profunda del zócalo", "Pasa una bayetilla húmeda para retirar el polvo y la grasa acumulada en la moldura.", "La superficie debe estar completamente seca antes de aplicar pintura."),
        ("task_retocar_zocalos", 2, "Enmascarado protector del piso", "Coloca cinta de enmascarar pegada al borde exacto entre el piso y el zócalo.", "Presiona firmemente la cinta con el dedo para evitar filtraciones debajo."),
        ("task_retocar_zocalos", 3, "Aplicación con brocha fina", "Aplica el esmalte en pasadas horizontales continuas con poca carga de pintura.", "Mantén la muñeca firme para no tocar la pared superior."),
        ("task_retocar_zocalos", 4, "Retiro de cinta y secado", "Retira la cinta de papel con un ángulo de 45° inmediatamente tras la última mano.", "No pases trapero en el piso contiguo durante las siguientes 12 horas."),

        # --- PINTAR PUERTA ---
        ("task_pintar_puerta", 1, "Preparación y calzado de la puerta", "Abre la puerta y coloca una cuña debajo para inmovilizarla. Protege la chapa con cinta de enmascarar.", "Coloca cartón o plástico debajo de toda la hoja."),
        ("task_pintar_puerta", 2, "Lijado suave superficial", "Lija la superficie con grano 150 para matar el brillo del esmalte anterior y dar agarre.", "Limpia el polvillo con un trapo ligeramente humedecido con alcohol."),
        ("task_pintar_puerta", 3, "Pintado de molduras y bordes", "Comienza con brocha fina pintando los marcos perimetrales y los rebajes de las molduras.", "Trabaja de arriba hacia abajo sin dejar acumulaciones en las esquinas."),
        ("task_pintar_puerta", 4, "Pintado de paños planos con rodillo", "Usa el mini rodillo de espuma para aplicar una capa uniforme en las áreas planas grandes.", "Deja secar 4 horas antes de aplicar la segunda mano de acabado."),

        # --- TAPAR HUECOS ---
        ("task_resanar_agujeros", 1, "Limpiar el orificio", "Retira el polvo o restos de yeso suelto con la punta de la espátula.", "Un orificio limpio garantiza adherencia duradera del estuco."),
        ("task_resanar_agujeros", 2, "Cargar y presionar estuco", "Toma una pequeña porción de masilla con la espátula y presiona firmemente dentro de la cavidad.", "Aplica la espátula inclinada a 45 grados."),
        ("task_resanar_agujeros", 3, "Nivelar al ras de la pared", "Pasa la espátula limpia horizontalmente para retirar todo el sobrante sin ahuecar.", "Evita dejar montículos grandes que después cuesten lijar."),
        ("task_resanar_agujeros", 4, "Lijado suave y retoque", "Una vez seco (45 min), lija suavemente con lija #220 en movimientos circulares hasta sentir plano al tacto.", "Limpia el polvo blanco con un paño seco antes de aplicar pintura de retoque."),

        # --- REPARAR FISURA SUPERFICIAL ---
        ("task_reparar_grieta_superficial", 1, "Sanear y abrir ligeramente la fisura", "Con la esquina de una espátula o bisturí, abre suavemente la grieta en forma de 'V' para quitar material desprendido.", "Verifica que la grieta sea menor a 1 mm y no atraviese vigas estructurales."),
        ("task_reparar_grieta_superficial", 2, "Limpieza del surco", "Pasa una brocha seca para retirar todo el polvillo del interior de la fisura.", "Si queda polvo dentro, la masilla elastomérica no se adherirá correctamente."),
        ("task_reparar_grieta_superficial", 3, "Colocación de malla y primera mano", "Pega la cinta de malla de fibra de vidrio centrada sobre la fisura y aplica la primera capa de masilla elástica.", "Presiona para que la masilla penetre a través de los poros de la malla."),
        ("task_reparar_grieta_superficial", 4, "Segunda mano de acabado y desvanecido", "Deja secar 2 horas y aplica una segunda mano ancha con espátula, desvaneciendo los bordes hacia el muro.", "Lija con suavidad para igualar el nivel de la pared existente."),

        # --- FIJAR ESQUINERO DRYWALL ---
        ("task_fijar_esquinero_drywall", 1, "Corte y remoción del sector dañado", "Corta con bisturí la zona de masilla agrietada y retira el segmento de metal doblado.", "Usa guantes de trabajo para evitar cortadas con bordes de lámina."),
        ("task_fijar_esquinero_drywall", 2, "Fijación del nuevo perfil esquinero", "Atornilla el esquinero galvanizado a los parantes asegurando que quede a 90 grados exactos.", "Comprueba la verticalidad con un nivel de burbuja."),
        ("task_fijar_esquinero_drywall", 3, "Empaste con masilla de juntas", "Aplica masilla de drywall con espátula ancha cubriendo los orificios del perfil metálico.", "Cubre unos 10 cm hacia cada lado de la esquina."),
        ("task_fijar_esquinero_drywall", 4, "Lijado y emparejado", "Deja secar 4 horas y lija con grano #150 hasta obtener una esquina recta y lisa.", "Aplica sellador fijador antes de la pintura final."),

        # --- INSTALAR REPISA ---
        ("task_instalar_repisa", 1, "Medición y trazado con nivel", "Ubica la altura deseada y marca los puntos de fijación trazando una línea recta con el nivel de burbuja.", "Verifica que no haya tomas de corriente alineadas verticalmente con los puntos."),
        ("task_instalar_repisa", 2, "Perforación con taladro percutor", "Usa broca para mampostería de 5/16\" a velocidad media, manteniendo el taladro perpendicular al muro.", "Usa gafas de seguridad para proteger los ojos del polvillo."),
        ("task_instalar_repisa", 3, "Inserción de chazos y soportes", "Inserta los chazos plásticos al ras del muro y atornilla las varillas de soporte con llave o alicate.", "Los chazos deben entrar ajustados sin bailar en el orificio."),
        ("task_instalar_repisa", 4, "Montaje y verificación de carga", "Desliza la repisa de madera sobre los soportes invisibles hasta topar con la pared. Verifica el nivel.", "Comprueba que soporte peso moderado antes de colocar objetos frágiles."),

        # --- COLGAR CUADROS ---
        ("task_colgar_cuadros", 1, "Definir posición y altura ergonómica", "Sujeta el cuadro contra la pared a la altura de los ojos (1.50 m del piso) y marca la parte superior con lápiz.", "Usa cinta de papel para no manchar el muro con el lápiz."),
        ("task_colgar_cuadros", 2, "Marcar punto exacto del anclaje", "Mide la distancia desde el marco hasta el alambre o cáncamo trasero tenso y descuéntala de la marca.", "Verifica que el punto esté nivelado si vas a colgar más de un cuadro."),
        ("task_colgar_cuadros", 3, "Fijar el gancho o clavo acerado", "Coloca el gancho de cuadro e introduce el clavo en ángulo de 45° con golpes firmes y suaves de martillo.", "El ángulo hacia abajo asegura que el peso del marco presione hacia la pared."),
        ("task_colgar_cuadros", 4, "Colgar y nivelar", "Suspende el cuadro sobre el gancho y ajusta la inclinación colocando un nivel pequeño sobre el marco.", "Retira la marca de lápiz suavemente con borrador de nata."),

        # --- INSTALAR CORTINERO ---
        ("task_instalar_cortinero", 1, "Marcación simétrica en ventana", "Mide entre 10 y 15 cm por encima del marco superior y 10 cm hacia afuera de los costados.", "La simetría es clave para que la cortina cubra la ventana por completo."),
        ("task_instalar_cortinero", 2, "Perforación e inserción de anclajes", "Perfora los orificios con broca de 5/16\" e introduce chazos de expansión resistentes.", "Si el muro es drywall, usa obligatoriamente chazos mariposa."),
        ("task_instalar_cortinero", 3, "Atornillado de soportes", "Fija los soportes metálicos asegurando los tornillos con destornillador manual.", "Verifica con el nivel que ambos soportes estén a la misma altura exacta."),
        ("task_instalar_cortinero", 4, "Montaje de barra y cortina", "Pasa las argollas o la tela por el tubo, encaja la barra en los soportes y ajusta los tornillos prisioneros.", "Asegura los terminales decorativos en los extremos."),

        # --- CAMBIAR BOMBILLO / PLAFÓN ---
        ("task_cambiar_bombillo", 1, "Corte de energía en el tablero general", "Baja el interruptor automático (breaker) correspondiente al circuito de iluminación en la caja de tacos.", "Intenta encender el interruptor de la habitación para confirmar que no hay luz."),
        ("task_cambiar_bombillo", 2, "Retiro del bombillo o plafón antiguo", "Desatornilla el bombillo frío con la mano. Si vas a cambiar la roseta, suelta los 2 tornillos de fijación a la caja.", "No toques los cables pelados con las manos desnudas."),
        ("task_cambiar_bombillo", 3, "Conexión de la nueva roseta de porcelana", "Conecta el cable neutro (blanco o azul) al borne de la rosca exterior y la fase al contacto central.", "Aprieta firmemente los tornillos prisioneros para que no haya falsos contactos."),
        ("task_cambiar_bombillo", 4, "Fijación y reenergización", "Fija la roseta a la caja octogonal, enrosca el bombillo LED, sube el breaker y comprueba el encendido.", "Verifica que el plafón no quede torcido ni con holguras."),

        # --- CAMBIAR INTERRUPTOR ---
        ("task_cambiar_interruptor", 1, "Desconexión total de energía", "Baja el breaker general de iluminación. Comprueba con buscapolo que no haya corriente en el tomacorriente vecino.", "Nunca trabajes en interruptores con el circuito energizado."),
        ("task_cambiar_interruptor", 2, "Desmontar la placa antigua", "Retira la tapa embellecedora haciendo palanca y desatornilla los 2 tornillos que sujetan el bastidor a la pared.", "Extrae los cables suavemente sin tirar de golpe."),
        ("task_cambiar_interruptor", 3, "Conectar los bornes del nuevo interruptor", "Conecta el cable de fase (línea) al borne marcado 'L' y el cable de retorno de lámpara al borne '1'.", "Asegúrate de que no queden hilos de cobre expuestos fuera del borne."),
        ("task_cambiar_interruptor", 4, "Atornillar bastidor y poner placa", "Introduce los cables con holgura en la caja, atornilla el chasis nivelado y calza la placa a presión.", "Sube el breaker en el tablero y prueba el encendido suave."),

        # --- CAMBIAR EMPAQUE GRIFO ---
        ("task_cambiar_empaque_grifo", 1, "Cerrar suministro de agua", "Cierra la llave de escuadra debajo del mueble o la llave general del baño.", "Abre el grifo para verificar que no salga más agua y pon el tapón en el desagüe."),
        ("task_cambiar_empaque_grifo", 2, "Desmontar la manija del grifo", "Retira la tapita embellecedora y afloja el tornillo central con destornillador.", "Guarda el tornillo y la manija sobre una toalla limpia."),
        ("task_cambiar_empaque_grifo", 3, "Extraer el vástago y cambiar empaque", "Desenrosca el vástago hexagonal con llave expansiva y sustituye el cuerito o empaque desgastado por uno nuevo.", "Aplica una vuelta de teflón en la rosca si observas holgura."),
        ("task_cambiar_empaque_grifo", 4, "Reensamblar y probar estanqueidad", "Vuelve a armar todo, abre la llave de paso lentamente y comprueba que cierre herméticamente.", "Verifica que el grifo no gotee ni por la boquilla ni por el eje de la manija."),

        # --- LIMPIAR SIFÓN ---
        ("task_limpiar_sifon", 1, "Colocar balde recolector", "Ubica un balde directamente debajo del sifón para recibir el agua y sedimentos que caerán al abrirlo.", "Usa guantes de caucho para higiene personal."),
        ("task_limpiar_sifon", 2, "Desenroscar tuercas de unión", "Gira las tuercas plásticas con las manos en sentido antihorario. Si están duras, usa un trapo seco para mejor agarre.", "No utilices llaves metálicas con fuerza excesiva para no partir las roscas de PVC."),
        ("task_limpiar_sifon", 3, "Limpieza de sedimentos y cabellos", "Vacía el contenido en el balde y limpia el interior del sifón con un cepillo y agua jabonosa.", "Revisa que los empaques cónicos de goma no estén agrietados ni deformes."),
        ("task_limpiar_sifon", 4, "Reinstalación y prueba de flujo", "Vuelve a colocar el sifón asegurando que los empaques queden bien sentados y aprieta las tuercas a mano.", "Abre el grifo con abundante caudal y confirma que no caiga ni una gota en las uniones."),

        # --- AJUSTAR BISAGRA MUEBLE ---
        ("task_ajustar_bisagra", 1, "Identificar el desalineamiento", "Cierra la puerta del mueble y observa si la puerta está caída, hundida o rozando con la vecina.", "Inspecciona si los tornillos de fijación a la madera están sueltos."),
        ("task_ajustar_bisagra", 2, "Ajustar tornillo de altura (vertical)", "Afloja ligeramente los dos tornillos del soporte en el mueble, sube o baja la puerta y vuelve a apretar.", "Haz este ajuste en ambas bisagras simultáneamente."),
        ("task_ajustar_bisagra", 3, "Ajustar tornillo lateral (izquierda/derecha)", "Gira el tornillo frontal de la bisagra en sentido horario para mover la puerta hacia el interior o viceversa.", "Gira en cuartos de vuelta comprobando el cierre cada vez."),
        ("task_ajustar_bisagra", 4, "Ajustar tornillo de profundidad", "Afloja el tornillo trasero para que la puerta no quede demasiado pegada al cuerpo del mueble y aprieta firme.", "Coloca un tope de silicona adhesivo para amortiguar el cierre."),

        # --- LUBRICAR CERRADURA ---
        ("task_lubricar_cerradura", 1, "Limpiar la llave y la ranura", "Limpia la llave con un paño seco para eliminar grasa vieja o pelusas.", "Introduce la punta del soplador para expulsar el polvo de la cerradura."),
        ("task_lubricar_cerradura", 2, "Aplicar grafito en polvo", "Coloca la boquilla del dosificador de grafito en la ranura de la llave y presiona suavemente dos veces.", "El polvo de grafito es un lubricante seco ideal que no atrapa mugre."),
        ("task_lubricar_cerradura", 3, "Distribuir el lubricante con la llave", "Introduce y saca la llave varias veces, y luego gírala en ambos sentidos para repartir el grafito en los pernos.", "Limpia los restos de polvo negro de la llave con papel absorbente."),
        ("task_lubricar_cerradura", 4, "Lubricar el pestillo y resbalón", "Aplica una gota de lubricante seco en el resbalón metálico y presiónalo con el dedo varias veces.", "Comprueba que la puerta cierre y abra sin necesidad de empujarla con el cuerpo."),

        # --- CORREDERA DE CAJÓN ---
        ("task_reparar_corredera_cajon", 1, "Extraer el cajón del mueble", "Hala el cajón hacia afuera y presiona las pestañas plásticas laterales hacia arriba y abajo para liberar el riel.", "Apoya el cajón en una superficie limpia y despejada."),
        ("task_reparar_corredera_cajon", 2, "Desatornillar los rieles dañados", "Retira los tornillos que sujetan el riel al cajón y al lateral del mueble con destornillador de estrella.", "Revisa que los orificios de la madera no estén rotos."),
        ("task_reparar_corredera_cajon", 3, "Presentar y atornillar nuevos rieles", "Coloca el nuevo riel telescópico alineado con el borde del mueble y fíjalo con los tornillos suministrados.", "Usa una escuadra para asegurar que el riel quede perfectamente horizontal."),
        ("task_reparar_corredera_cajon", 4, "Encajar el cajón y probar", "Empareja las guías del cajón con los rieles del mueble y empuja firmemente hasta escuchar el 'clic' de encastre.", "Abre y cierra el cajón tres veces comprobando que deslice con suavidad."),

        # --- RENOVAR SILICONA ---
        ("task_renovar_silicona", 1, "Retirar la silicona vieja y moho", "Corta con bisturí el cordón antiguo desprendiéndolo completamente de la loseta y del lavamanos o ducha.", "No dejes restos gomosos ni moho en la junta."),
        ("task_renovar_silicona", 2, "Limpieza profunda con alcohol", "Limpia la unión con un paño empapado en alcohol y seca con toalla de papel.", "La superficie debe estar 100% seca para que la silicona selle herméticamente."),
        ("task_renovar_silicona", 3, "Delimitar con cinta de enmascarar", "Coloca dos líneas de cinta paralelas dejando una franja libre de 5 mm en la junta.", "La cinta garantiza bordes rectos y limpios sin manchar la cerámica."),
        ("task_renovar_silicona", 4, "Aplicar cordón y perfilar", "Aplica el cordón continuo con la pistola y alisa inmediatamente con el dedo humedecido en agua jabonosa.", "Retira la cinta de enmascarar antes de que la silicona forme película y deja secar 24 horas sin mojar."),

        # --- DESCALCIFICAR DUCHA ---
        ("task_descalcificar_ducha", 1, "Preparar bolsa con vinagre", "Llena una bolsa plástica hermética hasta la mitad con vinagre blanco puro.", "El vinagre disuelve el sarro mineral de cal sin dañar el cromado."),
        ("task_descalcificar_ducha", 2, "Sumergir la regadera", "Envuelve la regadera de la ducha dentro de la bolsa asegurándola al cuello del tubo con una banda elástica firme.", "Asegúrate de que todas las boquillas queden sumergidas en el líquido."),
        ("task_descalcificar_ducha", 3, "Tiempo de reposo desincrustante", "Deja actuar el vinagre durante 3 a 4 horas (o toda la noche si el taponamiento es severo).", "Verás cómo se desprenden cristales blancos de calcio."),
        ("task_descalcificar_ducha", 4, "Cepillado y enjuague a presión", "Retira la bolsa, frota las boquillas de goma con un cepillo de dientes suave y abre la llave al máximo durante 1 minuto.", "Comprueba que todos los chorros salgan rectos y con presión plena."),

        # --- CAMBIAR HERRAJE SANITARIO ---
        ("task_cambiar_herraje_sanitario", 1, "Cerrar suministro y vaciar tanque", "Cierra la llave de escuadra del inodoro y baja la palanca manteniendo presionado para descargar toda el agua.", "Retira el remanente de agua del fondo del tanque con una esponja."),
        ("task_cambiar_herraje_sanitario", 2, "Desmontar la torre de entrada de agua", "Desconecta la manguera flexible y desenrosca la tuerca plástica inferior que fija la válvula al tanque.", "Ten un recipiente pequeño debajo por si gotea agua remanente."),
        ("task_cambiar_herraje_sanitario", 3, "Instalar nueva torre y graduar flotador", "Coloca el nuevo herraje con su empaque cónico en el fondo, aprieta la tuerca y conecta la manguera flexible.", "Gradúa la altura del flotador 2 cm por debajo del rebose."),
        ("task_cambiar_herraje_sanitario", 4, "Cambiar el sapo y probar descarga", "Engancha el nuevo sapo de silicona a las orejas del tubo y ajusta la cadena a la palanca con 1 cm de holgura.", "Abre la llave de paso, deja llenar y comprueba que cierre sin ningún goteo."),

        # --- LIMPIAR FILTROS CAMPANA ---
        ("task_limpiar_filtros_campana", 1, "Desmontar filtros metálicos", "Presiona la pestaña plástica o pestillo de cada rejilla y deslízala suavemente hacia abajo.", "Ten cuidado de no doblar el marco de aluminio."),
        ("task_limpiar_filtros_campana", 2, "Baño en agua caliente y bicarbonato", "Coloca los filtros en un platón con agua muy caliente, 1 taza de bicarbonato y 3 cucharadas de desengrasante.", "Deja actuar durante 20 minutos para ablandar la grasa adherida."),
        ("task_limpiar_filtros_campana", 3, "Cepillado suave no abrasivo", "Frota las mallas con un cepillo de cerdas suaves sin usar esponjas metálicas que puedan romper el filtro.", "Enjuaga con abundante agua tibia limpia."),
        ("task_limpiar_filtros_campana", 4, "Secado y montaje", "Deja secar los filtros apoyados en vertical sobre un paño y vuelve a encajarlos en la campana.", "Comprueba que la succión recupere su potencia habitual."),

        # --- REVISAR HUMEDADES ---
        ("task_revisar_humedades", 1, "Comprobación de sequedad en el muro", "Asegúrate de que la gotera o fuga origen ya fue reparada y que el muro esté completamente seco al tacto.", "Si el muro sigue húmedo, cualquier pintura se soplará en pocos días."),
        ("task_revisar_humedades", 2, "Tratamiento fungicida de moho", "Pasa una solución de agua con cloro o fungicida para neutralizar esporas de hongos y deja secar 2 horas.", "Usa guantes y ventila ampliamente la habitación."),
        ("task_revisar_humedades", 3, "Aplicación de sellador bloqueador", "Aplica una mano generosa de pintura bloqueadora de manchas base solvente sobre la aureola amarilla.", "Este sellador evita que la salitre traspase la pintura final."),
        ("task_revisar_humedades", 4, "Segunda mano y pintura de acabado", "Aplica la segunda mano del bloqueador y finaliza con dos manos del vinilo del color del cuarto.", "El muro quedará blanco y protegido contra rebrotes.")
    ]

    cursor.execute("DELETE FROM task_steps")
    for stp in steps:
        cursor.execute("""
            INSERT INTO task_steps (task_id, step_number, title, instructions, safety_tip)
            VALUES (?, ?, ?, ?, ?)
        """, stp)

    # 7. Proyectos y Favoritos de Prueba para el usuario Karla Polanco
    cursor.execute("DELETE FROM user_projects WHERE user_id = ?", (user_id,))

    sample_projects = [
        # 1. En progreso activo (Pintar sala)
        (
            user_id, "task_pintar_pared", "Pintar sala principal",
            "Fase 2: Segunda mano de vinilo", "en_progreso", 65, 14.5, "recom", 185000,
            "Vinilo Tipo 1 tono marfil adquirido en ferretería del barrio. Se aplicó la primera mano el sábado.", 1
        ),
        # 2. En progreso (Instalar repisas)
        (
            user_id, "task_instalar_repisa", "Instalar repisas flotantes en estudio",
            "Fase 1: Trazado y perforación", "en_progreso", 30, 2.0, "recom", 48000,
            "Comprar chazos de expansión 5/16 y prestar nivel de burbuja a mi cuñado.", 1
        ),
        # 3. Completado (Tapar huecos)
        (
            user_id, "task_resanar_agujeros", "Tapar huecos de cuadros en pasillo",
            "Completado con éxito", "completado", 100, 1.0, "recom", 18000,
            "Se taparon 8 orificios dejados por los cuadros viejos. Lijado y retocado impecable.", 1
        ),
        # 4. Completado (Cambio bombillo balcón)
        (
            user_id, "task_cambiar_bombillo", "Cambiar plafón y bombillo en balcón",
            "Completado con éxito", "completado", 100, 1.0, "recom", 15000,
            "Se bajó el breaker general antes de manipular. Se instaló bombillo LED de 9W luz cálida.", 0
        ),
        # 5. Planeado (Sellar ducha)
        (
            user_id, "task_renovar_silicona", "Sellar junta de ducha baño social",
            "Presupuesto calculado", "planeado", 0, 1.0, "recom", 24000,
            "Retirar la silicona negra con bisturí y limpiar con alcohol antes de calafatear.", 1
        ),
        # 6. Planeado (Cambiar empaque grifo)
        (
            user_id, "task_cambiar_empaque_grifo", "Cambiar empaque grifo lavaplatos",
            "Presupuesto calculado", "planeado", 0, 1.0, "recom", 12000,
            "El grifo presenta goteo continuo de 1 gota cada 5 segundos. Comprar juego universal de nitrilo.", 0
        )
    ]

    for p in sample_projects:
        cursor.execute("""
            INSERT INTO user_projects (
                user_id, task_id, project_name, phase_name, status,
                progress_percent, area_m2, tier_selected, calculated_cost_cop,
                notes, is_favorite
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    conn.commit()
    conn.close()
    print("Base de datos de CasaLista inicializada y sembrada con éxito con todos los módulos.")

if __name__ == "__main__":
    from app.database import init_db
    init_db()
    seed_database()
