from common.facebook import update_messenger_profile

project_menu =
"payload": {
  "template_type": "generic",
  "elements": [
    {
      "title": "Your Project",
      "image_url": "http://via.placeholder.com/250x250",
      "webview_height_ratio": "full"          
      "buttons": [
              {
                "title": "Select",
                "type": "postback",
                "payload": "<PROJECT_ID>"            
              }
            ]
    },


attachments = {
    "type":"template",
    "payload":{
      "template_type":"generic",
      "elements":[
        {
          "title": "Your Project",
          "subtitle": 'Tags'
          "image_url": "http://via.placeholder.com/250x250",
          "webview_height_ratio": "full"          
          "buttons": [
                  {
                    "title": "Select",
                    "type": "postback",
                    "payload": "<PROJECT_ID>"            
                  }
                ]
        },
        {
          "title": "Select More",
          "image_url": "http://via.placeholder.com/250x250",
          "webview_height_ratio": "full"          
          "buttons": [
                  {
                    "title": "Select",
                    "type": "postback",
                    "payload": "GET_MORE_1"            
                  }
                ]
        },
      ]
    }
}