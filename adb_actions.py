import subprocess
import time
import cv2

def capture_screen_and_save(local_path, image_out, device_id=None):
    adb_command(f"shell screencap -p /sdcard/{image_out}.png", device_id)

    adb_command(f"pull /sdcard/{image_out}.png {local_path}", device_id)

def find_pattern(image_path, template_path, threshold=0.8):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)


    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        w, h = template.shape[::-1]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return center_x, center_y
    else:
        return None
def adb_command(command, device_id=None):
    adb_prefix = f"adb -s {device_id}" if device_id else "adb"
    full_command = f"{adb_prefix} {command}"

    process = subprocess.Popen(full_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output, error

def capture_screen_and_save(local_path, image_out, device_id=None):
    adb_command(f"shell screencap -p /sdcard/{image_out}.png", device_id)

    adb_command(f"pull /sdcard/{image_out}.png {local_path}", device_id)

def click_on_pos(x,y, device_id=None):
    adb_command(f"shell input tap {x} {y}", device_id)

def adb_input_text(text_to_write, device_id=None):
    adb_prefix = f"adb -s {device_id}" if device_id else "adb"
    full_command = f"{adb_prefix} shell input text '{text_to_write}'"

    process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        print(f"Error: {error.decode('utf-8')}")
    else:
        print("Texto ingresado correctamente.")

def adb_delete_text(cant_car, device_id=None):
    for i in range(cant_car):
        adb_command("shell input keyevent KEYCODE_DEL", device_id)
        time.sleep(0.05)


def abrirMenuTropas(mainID):
    capture_screen_and_save('./adb_data/screenshots/', "screenshot", mainID)
    filasExpand = find_pattern('./adb_data/screenshots/screenshot.png', './adb_data/patrons/expand_troops.png', threshold=0.8)

    if filasExpand:
        click_on_pos(filasExpand[0], filasExpand[1], mainID)
        return True

    else:
        print("Expandir a menú de tropas no encontrado")
        return False

def nevskyEnTropas(mainID):
    capture_screen_and_save('./adb_data/screenshots/', "screenshot", mainID)
    nevsky = find_pattern('./adb_data/screenshots/screenshot.png', './adb_data/patrons/nevsky_in_troopsMenu.png',
                               threshold=0.8)
    if nevsky:
        return True
    else:
        print("Nevsky vuelto")
        return False

def cerrarMenu(mainID):
    capture_screen_and_save('./adb_data/screenshots/', "screenshot", mainID)
    closeButton = find_pattern('./adb_data/screenshots/screenshot.png', './adb_data/patrons/troopsMenu_close.png',
                          threshold=0.8)
    if closeButton:
        click_on_pos(closeButton[0], closeButton[1], mainID)
        print("Si se cerró")
        return True
    else:
        print("No se cerró")
        return False

def entarAWarMenu(deviceID):
    capture_screen_and_save('./adb_data/screenshots/', "screenshot", deviceID)
    allianceButton = find_pattern('./adb_data/screenshots/screenshot.png', './adb_data/patrons/alliance_button.png',
                               threshold=0.8)
    if allianceButton:
        click_on_pos(allianceButton[0], allianceButton[1], deviceID)

        time.sleep(1)

        capture_screen_and_save('./adb_data/screenshots/', "screenshot", deviceID)
        warButton = find_pattern('./adb_data/screenshots/screenshot.png',
                                      './adb_data/patrons/war_button.png',
                                      threshold=0.8)
        if warButton:
            click_on_pos(warButton[0], warButton[1], deviceID)
            return True

    return False


def searchBarbarianFort(mainID):
    capture_screen_and_save('./adb_data/screenshots/', "screenshot", mainID)
    waypointButton = find_pattern('./adb_data/screenshots/screenshot.png', './adb_data/patrons/waypoint_button.png',
                                  threshold=0.8)

    if not waypointButton:
        waypointButton = find_pattern('./adb_data/screenshots/screenshot.png', './adb_data/patrons/waypoint_button_unread.png',
                                      threshold=0.8)

    if waypointButton:
        click_on_pos(waypointButton[0], waypointButton[1], mainID)
        time.sleep(1.5)

        capture_screen_and_save('./adb_data/screenshots/', "screenshot", mainID)
        waypointMenu = find_pattern('./adb_data/screenshots/screenshot.png', './adb_data/patrons/waypoint_menu_unmarked.png',
                                      threshold=0.8)
        if waypointMenu:
            click_on_pos(waypointMenu[0]-45, waypointMenu[1], mainID)
            time.sleep(1)

            capture_screen_and_save('./adb_data/screenshots/', "screenshot", mainID)
            waypointMenu_IrButton = find_pattern('./adb_data/screenshots/screenshot.png',
                                        './adb_data/patrons/waypoint_menu_ir_button.png',
                                        threshold=0.8)

            if waypointMenu_IrButton:
                click_on_pos(waypointMenu_IrButton[0], waypointMenu_IrButton[1], mainID)
            else:
                print("IrButton no encontrado")

def hayBarbarianFort(mainID):
    congregateButton = None
    for i in range(5):
        # print("Buscando barbarianFort: ", end="")
        click_on_pos(480, 270, mainID)
        time.sleep(1)
        capture_screen_and_save('./adb_data/screenshots/', "screenshot", mainID)
        congregateButton = find_pattern('./adb_data/screenshots/screenshot.png',
                                             './adb_data/patrons/barbarian_fort_congregate.png',
                                             threshold=0.8)
        if congregateButton:
            # print(f"Encontrado {i}")
            time.sleep(1)
            break
        # else:
        #     print(f"NO Encontrado {i}")

    if congregateButton:
        print("Se retorna Congregate")
        return congregateButton
    else:
        print("Se retorna False")
        return False

def borrarWaypoint(mainID):
    capture_screen_and_save('./adb_data/screenshots/', "screenshot", mainID)
    waypointButton = find_pattern('./adb_data/screenshots/screenshot.png', './adb_data/patrons/waypoint_button.png',
                                  threshold=0.8)

    if waypointButton:
        click_on_pos(waypointButton[0], waypointButton[1], mainID)
        time.sleep(1.5)

        capture_screen_and_save('./adb_data/screenshots/', "screenshot", mainID)
        waypointMenu = find_pattern('./adb_data/screenshots/screenshot.png',
                                    './adb_data/patrons/waypoint_menu_unmarked.png',
                                    threshold=0.8)
        if waypointMenu:
            click_on_pos(waypointMenu[0] - 45, waypointMenu[1], mainID)
            time.sleep(1)

            capture_screen_and_save('./adb_data/screenshots/', "screenshot", mainID)
            deleteButton = find_pattern('./adb_data/screenshots/screenshot.png',
                                                 './adb_data/patrons/waypoint_delete_button.png',
                                                 threshold=0.8)

            if deleteButton:
                click_on_pos(deleteButton[0], deleteButton[1], mainID)
            else:
                print("deleteButton no encontrado")

            cerrarMenu(mainID)

def congregar(mainID, congregateButton):
    print("Se hace click en ", congregateButton)
    click_on_pos(congregateButton[0], congregateButton[1], mainID)
    time.sleep(2)

    capture_screen_and_save('./adb_data/screenshots/', "screenshot", mainID)
    congregateFromMarch = find_pattern('./adb_data/screenshots/screenshot.png',
                                './adb_data/patrons/marches_congregate.png',
                                threshold=0.8)
    if congregateFromMarch:
        click_on_pos(congregateFromMarch[0], congregateFromMarch[1], mainID)
        time.sleep(2)

        capture_screen_and_save('./adb_data/screenshots/', "screenshot", mainID)
        selectOnePreset = find_pattern('./adb_data/screenshots/screenshot.png',
                                           './adb_data/patrons/marchSend_preset1.png',
                                           threshold=0.8)

        cavButton = find_pattern('./adb_data/screenshots/screenshot.png',
                                 './adb_data/patrons/marchSend_cav.png',
                                 threshold=0.8)

        if selectOnePreset:
            click_on_pos(selectOnePreset[0], selectOnePreset[1], mainID)
            time.sleep(2)

            capture_screen_and_save('./adb_data/screenshots/', "screenshot", mainID)
            selectMaximo = find_pattern('./adb_data/screenshots/screenshot.png',
                                           './adb_data/patrons/marchSend_maximo.png',
                                           threshold=0.8)
            if selectMaximo:
                click_on_pos(selectMaximo[0], selectMaximo[1], mainID)
                time.sleep(1)


        if cavButton:
            click_on_pos(cavButton[0] + 13, cavButton[1], mainID)

        time.sleep(0.5)

        marcha = find_pattern('./adb_data/screenshots/screenshot.png',
                                       './adb_data/patrons/marchSend_marcha.png',
                                       threshold=0.8)
        if marcha:
            click_on_pos(marcha[0], marcha[1], mainID)

def automatizarJoin(joinerID):
    capture_screen_and_save('./adb_data/screenshots/', "screenshot", joinerID)
    sinAP = find_pattern('./adb_data/screenshots/screenshot.png',
                               './adb_data/patrons/out_action_points.png',
                               threshold=0.8)
    if sinAP:

        return True
    time.sleep(1)


    esperarBack = None
    while True:
        capture_screen_and_save('./adb_data/screenshots/', "screenshot", joinerID)
        esperarBack = find_pattern('./adb_data/screenshots/screenshot.png',
                                    './adb_data/patrons/expand_troops.png',
                                    threshold=0.8)
        if not esperarBack:
            break
        else:
            time.sleep(2)

    allianceButton = find_pattern('./adb_data/screenshots/screenshot.png',
                               './adb_data/patrons/alliance_button.png',
                               threshold=0.8)
    if allianceButton:
        click_on_pos(allianceButton[0], allianceButton[1], joinerID)
        time.sleep(2)

        capture_screen_and_save('./adb_data/screenshots/', "screenshot", joinerID)
        warButton = find_pattern('./adb_data/screenshots/screenshot.png',
                                      './adb_data/patrons/war_button.png',
                                      threshold=0.8)

        if warButton:
            click_on_pos(warButton[0], warButton[1], joinerID)
            time.sleep(6)
            joinButton = None

            while not joinButton:

                capture_screen_and_save('./adb_data/screenshots/', "screenshot", joinerID)
                joinButton = find_pattern('./adb_data/screenshots/screenshot.png',
                                         './adb_data/patrons/rallyMenu_join.png',
                                         threshold=0.8)

                if joinButton:
                    click_on_pos(joinButton[0], joinButton[1], joinerID)
                    time.sleep(4)

                    capture_screen_and_save('./adb_data/screenshots/', "screenshot", joinerID)
                    newTroops = find_pattern('./adb_data/screenshots/screenshot.png',
                                               './adb_data/patrons/marches_newTroops.png',
                                               threshold=0.8)
                    if newTroops:
                        click_on_pos(newTroops[0], newTroops[1], joinerID)
                        time.sleep(2)


                        capture_screen_and_save('./adb_data/screenshots/', "screenshot", joinerID)
                        marchButton = find_pattern('./adb_data/screenshots/screenshot.png',
                                                  './adb_data/patrons/joinPlayer_march.png',
                                                  threshold=0.8)

                        if marchButton:
                            click_on_pos(marchButton[0], marchButton[1], joinerID)
                            time.sleep(1)
                            return False
                else:
                    time.sleep(2)




def automatizarMain(mainID, joinerID):
    while True:
        capture_screen_and_save('./adb_data/screenshots/', "screenshot", joinerID)
        sinAP = find_pattern('./adb_data/screenshots/screenshot.png',
                             './adb_data/patrons/out_action_points.png',
                             threshold=0.8)
        if sinAP:
            return "MAIN SIN AP"
        time.sleep(1)

        is_nevskyInTropas = True
        while is_nevskyInTropas:
            is_nevskyInTropas = nevskyEnTropas(mainID)

            if is_nevskyInTropas:
                time.sleep(5)
        cerrarMenu(mainID)
        time.sleep(1)
        searchBarbarianFort(mainID)
        time.sleep(5)

        congregateButton = hayBarbarianFort(mainID)

        if congregateButton:
            time.sleep(1)
            congregar(mainID, congregateButton)
            time.sleep(10)
            borrarWaypoint(mainID)
            time.sleep(3)
            abrirMenuTropas(mainID)
            time.sleep(1)

            outAP = automatizarJoin(joinerID)
            if outAP:
                return "JOINER SIN AP"

        else:
            borrarWaypoint(mainID)
            time.sleep(2)



def automatizar(mainID, joinerID):
    abrirMenuTropas(mainID)
    time.sleep(1)

    sinAP = automatizarMain(mainID, joinerID)
    if sinAP:
        print(sinAP)
