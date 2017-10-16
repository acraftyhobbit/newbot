from common.facebook import update_messenger_profile




home_menu =[
  {
    "locale":"default",
    "composer_input_disabled": True,
    "call_to_actions":[
      {
            "title":"New Project",
            "type":"postback",
            "payload":"ADD_PROJECT_PAYLOAD"
          },
       {
            "title":"Update Project",
            "type":"postback",
            "payload":"UPDATE_PROJECT_PAYLOAD"
          }, 
      {
        "title":"Add Supplies",
        "type":"nested",
        "call_to_actions":[
          {
            "title":"Add Pattern",
            "type":"postback",
            "payload":"ADD_PATTERN_PAYLOAD"
          },
          {
            "title":"Add Material",
            "type":"postback",
            "payload":"ADD_MATERIAL_PAYLOAD"
          },
        ]
      },
    ]
  }
]

r = update_messenger_profile(persistent_menu= home_menu)