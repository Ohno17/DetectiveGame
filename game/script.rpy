
define narrator = Character(None, what_italic=True)
define d = Character("Detective", color="#c8ffc8")
define s = Character("Security", color="#161351")

# Names
define DETECTIVE_NAME = "Sam Arragena"
define SECURITY_NAME = "Paris Konji"

# Items
define HOUSE_KEY = "the house keys"
define GLASS = "an empty drinking glass"
define BLOOD_GLASS = "a drinking glass with some dried blood"
define DETECTIVE_ID = "my detective ID"

default items = []

# Story progression
default been_to_hub = False
default been_to_alleyway = False
default been_to_house = False
default been_to_house_entrance = False
default been_to_detective_station = False

default house_entrance_manual_unlock = False
default house_noticed_car_keys_missing = False
default detective_station_checked_id = False
default detective_station_analyzed_blood = False

transform left:
    xalign 0.0
    xanchor 0.0
    zoom 0.5

transform right:
    xalign 1.0
    xanchor 1.0
    zoom 0.5

label start:
    jump start_alley_scene

label start_alley_scene:

    scene brickwall

    show detective at left
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

    show detective at left
    d "Let's see here... I have: [string_items]."
    hide detective

    return

label hub_scene:

    scene brickwall with fade

    if not been_to_hub:
        "The detective finds themselves in a familiar city."

        play music surrealexploration

        show detective at left
        d "The streets feel empty, today."
        d "... and I can't just disregard how I randomly woke up in that alley. Come to think of it, I can't really remember how I got there."
        hide detective

        $ been_to_hub = True

    label .options:
        menu:
            "What should I do?"

            "Look around":
                show detective at left
                d "I see some buildings and a few closed shops. Nothing seems out of the ordinary. There's the alleyway to the left, the detective station ahead, and my house to the right."
                hide detective
                jump .options
            
            "Leave the street":
                show detective at left

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
        
        show detective at left
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
                show detective at left
                d "There's a wire fence blocking me from going further, not that I would want to... in the dark... To the right and left are the brick walls of the neighboring buildings, with no doors in sight. On the floor is some dried blood, and..."
                d "wow, that blood's real creepy."
                hide detective
                jump alleyway_options
            
            "Inspect the blood on the ground":
                show detective at left
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
        
        show detective at left
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
                show detective at left
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
                    show detective at left
                    d "I have my keys now, so I can unlock the door to my own home, I hope."
                    "The ring of keys jingle together, and after a little bit of struggle..."
                    pause 2
                    hide detective
                    $ house_entrance_manual_unlock = True
                    jump home_scene
                else:
                    show detective at left
                    d "Not really sure how to do this without any keys. I'm a detective! Not a locksmith..."
                    hide detective
                    jump .options
            
            "Check items":
                call check_inventory
                jump .options

label home_scene:

    scene brickwall with fade

    if not been_to_house:

        show detective at left
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
                show detective at left
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
                show detective at left
                d "It's not here..."
                pause 1.0
                d "Well, that's going to make things a little harder. Can't even drive down to the hotel to stay overnight... I guess I'm not going to do much sleeping until I've figured out what's happening, though..."
                $ house_noticed_car_keys_missing = True
                hide detective
                jump .options
            
            "Check for the silverware":
                "Broken ceramic and glass is strewn all across the floor."

                show detective at left
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
                show detective at left
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
        show detective at left
        d "I feel like I haven't been here in a while..."
        d "Hope they still recongnize me."
        pause 0.5
        "The Detective tries to enter the back rooms, but..."
        show security at right
        s "Hey! You haven't checked your I.D. yet, and I can't have random people walking in!"
        d "Oh... sorry, but... don't you recongnize me? I'm the investigator at this station."
        s "Even if I did, it's protocol. Unfortunately, I don't recongnize you either."
        hide security
        d "Maybe they're just new... I gotta check in with my I.D. card then."
        hide detective

        $ been_to_detective_station = True
    
    label .options:
        menu:
            "What should I do?"

            "Leave the station":
                jump hub_scene
            
            "Look around":
                show detective at left
                d "Let's see here... there should be a blood analyzer machine around here."
                d "There's also the security guard at the front desk."
                hide detective
                jump .options
            
            "Check in with the guard" if not detective_station_checked_id:
                show detective at left
                show security at right
                if DETECTIVE_ID in items:
                    d "Here's my card."
                    "The Detective extends their hand, containing the simple I.D. card. On the card is a barcode along the long side, and a picture."
                    g "Thanks, and you're allowed in now."
                    $ detective_station_checked_id = True
                else:
                    d "I still don't have my I.D. card. Is there really no other way?"
                    g "Nope. Sorry, I can't just allow any random person to come in, and you are no exception."
                hide detective
                hide security
                jump .options
            
            "Go to the analysis lab" if detective_station_checked_id and (not detective_station_analyzed_blood):
                show detective at left
                if BLOOD_GLASS in items:
                    "The detective places the glass into the machine, and it buzzes to life. After a few seconds, it prints out the results."
                    d "So the person this blood belonged to is..."
                    pause 1.5
                    play music tevottwisbos
                    d "is... me?"
                    $ detective_station_analyzed_blood = True
                    show security at right
                    s "That's some weird sample you've brought... Did you really need to analyze your own blood."
                    pause 1.0
                    menu:
                        "What do I say?"

                        "Checking if the machine is working":
                            d "Heh... Yeah! J-just checking if the machine is working right now... you know."
                            s "I see..."
                        "Curious about the results.":
                            d "Y-Yeah! Just... curious about the results of my own blood!"
                            s "I see..."
                        "Training myself":
                            d "Yup! Just, you knokw... training myself on how to use the machine."
                            s "Didn't you say I should have recongnized you?"
                            d "Yes... well..."
                    s "Well, make sure to clean up the machine afterward. It messes up results if the area is unsanitary."
                    d "Yes, will do."
                    hide security
                    d "That was close... why did I lie? I guess I've solved the mystery of who this belonged to"
                else:
                    d "I don't really have anything to analyse right now."
                hide detective
                jump .options

            "Check items":
                call check_inventory
                jump .options
