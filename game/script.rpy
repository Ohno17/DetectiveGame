
define narrator = Character(None, what_italic=True)
define d = Character("Detective", color="#c8ffc8")
define s = Character("Security", color="#161351")

define HOUSE_KEY = "the house keys"
define GLASS = "an empty drinking glass"
define BLOOD_GLASS = "a drinking glass with some dried blood"
define DETECTIVE_ID = "my detective ID"

default items = []

default been_to_hub = False
default been_to_alleyway = False
default been_to_house = False
default been_to_house_entrance = False
default been_to_detective_station = False

default house_entrance_manual_unlock = False
default house_noticed_car_keys_missing = False

transform character_zoom: 
    zoom 0.5

label start:
    jump start_alley_scene

label start_alley_scene:

    scene brickwall

    show detective at character_zoom
    d "Oww... my head... Where am I?"
    d "The alley? Better get back home... I must have fallen asleep."
    hide detective

    jump hub_scene

label check_inventory:

    python:
        if len(items) > 0:
            string_items = ", ".join(items)
        else:
            string_items = "absolutely nothing"

    show detective at character_zoom
    d "Let's see here... I have: [string_items]."
    hide detective

    return

label hub_scene:

    scene brickwall with fade

    if not been_to_hub:
        "The detective finds themselves in a familiar city."

        play music surrealexploration

        show detective at character_zoom
        d "The streets feel empty, today."
        d "... and I can't just disregard how I randomly woke up in that alley. Come to think of it, I can't really remember how I got there."
        hide detective

        $ been_to_hub = True

    label .options:
        menu:
            "What should I do?"

            "Look around":
                show detective at character_zoom
                d "I see some buildings and a few closed shops. Nothing seems out of the ordinary. There's the alleyway to the left, the detective station ahead, and my house to the right."
                hide detective
                jump .options
            
            "Leave the street":
                show detective at character_zoom

                if been_to_house:
                    d "Something has happened here, and I need to know what..."
                    d "I can't leave right now."
                    jump .options

                if been_to_house_entrance:
                    d "I... can't leave right now. I need to get inside my house somehow!"
                    jump .options

                # Default at beginning of game
                d "It's dark outside! With nowhere else to be right now, my priority should be to find a way home."
                hide detective
                
                jump .options
            
            "Check items":
                call check_inventory
                jump .options

            "Explore alleyway":
                jump alleyway_scene
            "Explore home":
                jump home_entrance_scene
            "Explore detective station":
                jump detective_station_scene
        
        jump .options

label alleyway_scene:

    scene brickwall with fade

    if not been_to_alleyway:
        "The alleyway is dimly lit and narrow."
        
        show detective at character_zoom
        d "Feels more creepy than usual."
        d "And is... is that blood on the ground?"
        hide detective

        $ been_to_alleyway = True
    
    label alleyway_options:
        menu:
            "What should I do?"

            "Leave the alley":
                jump hub_scene
            
            "Look around":
                show detective at character_zoom
                d "There's a wire fence blocking me from going further, not that I would want to... in the dark... To the right and left are the brick walls of the neighboring buildings, with no doors in sight. On the floor is some dried blood, and..."
                d "wow, that blood's real creepy."
                hide detective
                jump alleyway_options
            
            "Inspect the blood on the ground":
                show detective at character_zoom
                d "A classic lead... if I found out who this belonged to, that is. Maybe I could collect for analysis it if I had some container?"

                if GLASS in items:
                    d "Oh! I have this glass from my house! I used this one for drinking, but..."

                    "The dried blood was collected into the glass"
                    python:
                        items.remove(GLASS)
                        items.append(BLOOD_GLASS)
                
                if HOUSE_KEY not in items:
                    "An unnatural shine in the blood caught the Detective's eye"
                    d "Also, there's something shiny here..."
                    d "Wait... these are my house keys? How did they end up here, in this mess?"
                    "The Detective picked the keys up"
                    $ items.append(HOUSE_KEY)
                
                hide detective
                jump alleyway_options
            
            "Check items":
                call check_inventory
                jump alleyway_options

label home_entrance_scene:

    if (HOUSE_KEY in items) and (not been_to_house_entrance):
        jump home_scene
    if house_entrance_manual_unlock:
        jump home_scene

    scene brickwall with fade

    if not been_to_house_entrance:
        
        show detective at character_zoom
        d "Ah... home sweet ho-"
        d "Wait... I don't have my keys! Where could they possibly be... I just woke up in some random place, and now my keys are missing as well!"
        hide detective

        $ been_to_house_entrance = True

    label .options:
        menu:
            "What should I do?"

            "Leave the house entrance":
                jump hub_scene
            
            "Look around":
                show detective at character_zoom
                d "It's not like I keep spares under my welcome mat..."
                "Just for the sake of their own sanity, the Detective checked under the welcome mat."
                d "There's a little paper note here:"
                "YOUR CONTRACT BROKEN, A BETRAYAL OF WHAT YOU PROMISED"
                pause 1.5
                d "..."
                hide detective
                jump .options
            
            "Try unlocking the door":
                if HOUSE_KEY in items:
                    show detective at character_zoom
                    d "I have my keys now, so I can unlock the door to my own home, I hope."
                    "The ring of keys jingle together, and after a little bit of struggle..."
                    pause 2
                    hide detective
                    $ house_entrance_manual_unlock = True
                    jump home_scene
                else:
                    show detective at character_zoom
                    d "Not really sure how to do this without any keys. I'm a detective! Not a locksmith..."
                    hide detective
                    jump .options
            
            "Check items":
                call check_inventory
                jump .options

label home_scene:

    scene brickwall with fade

    if not been_to_house:

        show detective at character_zoom
        d "Ahhh finally... home sweet ho-"
        "The house looks like a large cattle of mice trampled through it. The Detective is both shocked and confused."
        pause 1
        d "I don't remember it being this disorganized, wait... Did someone break into my house or something?"
        hide detective

        $ been_to_house = True
    
    label .options:
        menu:
            "What should I do?"

            "Leave the house":
                jump hub_scene
            
            "Check for the detective ID" if DETECTIVE_ID not in items:
                show detective at character_zoom
                if house_noticed_car_keys_missing:
                    d "At least this is still here... not that I've noticed anything else missing except my car keys. Stealing my car is a pretty big burglary itself, though..."
                else:
                    d "At least this is still here... not that I have noticed anything else missing."
                "The Detective picks up their identification card."
                $ items.append(DETECTIVE_ID)
                d "Seems like whoever came here had the goal to cause as much damage as possible."
                hide detective
                jump .options
            
            "Check for the car keys" if not house_noticed_car_keys_missing:
                show detective at character_zoom
                d "It's not here..."
                pause 1.0
                d "Well, that's going to make things a little harder. Can't even drive down to the hotel to stay overnight... I guess I'm not going to do much sleeping until I've figured out what's happening, though..."
                $ house_noticed_car_keys_missing = True
                hide detective
                jump .options
            
            "Check for the silverware":
                "Broken ceramic and glass is strewn all across the floor."

                show detective at character_zoom
                if (GLASS in items) or (BLOOD_GLASS in items):
                    d "Checking for the silverware again? I... I'm not really concerned about this right now."
                    if GLASS in items:
                        d "I've already got my glass, anyway."
                    if BLOOD_GLASS in items:
                        d "I've already got my glass full of samples, anyway."
                else:
                    d "Checking for the silverware? I... I'm not really concerned about this right now. I guess I could take a glass of water with me, I'm not sure when I'll come back home."
                    "The Detective took one of their favorite drinking glasses and stuffed it safely into their pocket."
                    $ items.append(GLASS)
                hide detective

                jump .options

            "Look around":
                show detective at character_zoom
                d "Let's see here... there should be my detective ID in a cupboard, my car keys on a stand... There is also the silverware that I use to eat, but I'm not really hungry right now."
                hide detective
                jump .options
            
            "Check items":
                call check_inventory
                jump .options


label detective_station_scene:

    scene brickwall with fade

    if not been_to_detective_station:

        "There stands a security guard at the front desk. Behind the guard is the lab where analysis is carried out. The waiting room of the station is empty, as usual."
        show detective at character_zoom
        d "I feel like I haven't been here in a while..."
        d "Hope they still recongnize me."
        hide detective

        $ been_to_detective_station = True
    
    label .options:
        menu:
            "What should I do?"

            "Leave the station":
                jump hub_scene
            
            "Look around":
                show detective at character_zoom
                d "Let's see here... there should be a blood analyzer machine around here."
                d "There's also the security guard at the front desk. It's "
                hide detective
                jump .options
            
            "Check the blood analyzer":
                show detective at character_zoom
                show security at character_zoom
                if DETECTIVE_ID in items:
                    s "May I see your I.D. please?"
                    d "Sure."
                    "The Detective's I.D. was scanned with a helpfully placed barcode along the long side."
                else:
                    s "Woah woah woah... I can't have you waltzing into here without your I.D."
                    d "I've been here before, don't you recongnize me?"
                    s "Sorry, no I.D., no entry."
                    "The Detective reaches into their pocket for their I.D...."
                    d "...seems like I've misplaced it..."
                    s "Then I'll be waiting until you find it. Until then, you're not allowed in."
                hide detective
                hide security
                jump .options


            "Check items":
                call check_inventory
                jump .options
