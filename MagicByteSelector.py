from burp import IBurpExtender, IContextMenuFactory, IContextMenuInvocation
from javax.swing import JMenuItem
from java.util import ArrayList

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Magic Byte Selector")
        callbacks.registerContextMenuFactory(self)
        
        print("This extension is made by https://websec.nl Research & Development Team,\n"
              "If you like this tool then please consider leaving us a positive google review\n"
              "and/or star our projects on GitHub. Happy hacking!")
    
    def createMenuItems(self, invocation):
        self._invocation = invocation

        # Check if the editor is writable
        context = self._invocation.getInvocationContext()
        if context not in [IContextMenuInvocation.CONTEXT_MESSAGE_EDITOR_REQUEST, 
                           IContextMenuInvocation.CONTEXT_MESSAGE_EDITOR_RESPONSE]:
            return None

        menuList = ArrayList()
        menuList.add(JMenuItem("Insert JPG Magic Byte", actionPerformed=lambda x: self.insertMagicBytes('JPG')))
        menuList.add(JMenuItem("Insert PNG Magic Byte", actionPerformed=lambda x: self.insertMagicBytes('PNG')))
        menuList.add(JMenuItem("Insert JPEG Magic Byte", actionPerformed=lambda x: self.insertMagicBytes('JPEG')))
        menuList.add(JMenuItem("Insert GIF89a Magic Byte", actionPerformed=lambda x: self.insertMagicBytes('GIF89a')))
        menuList.add(JMenuItem("Insert GIF87a Magic Byte", actionPerformed=lambda x: self.insertMagicBytes('GIF87a')))
        return menuList

    def insertMagicBytes(self, file_type):
        try:
            magic_bytes = {
                'JPG': b"\xFF\xD8\xFF",
                'PNG': b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A",
                'JPEG': b"\xFF\xD8\xFF\xE0",
                'GIF89a': b"\x47\x49\x46\x38\x39\x61",
                'GIF87a': b"\x47\x49\x46\x38\x37\x61",
            }

            # Get the selected data boundaries
            selection_bounds = self._invocation.getSelectionBounds()
            
            # Get the HTTP request and selected data
            byte_request = bytearray(self._invocation.getSelectedMessages()[0].getRequest())
            
            # Print the selection bounds and selected data for debugging
            print("Selection bounds: {}\nSelected data: {}".format(selection_bounds, byte_request[selection_bounds[0]:selection_bounds[1]]))
            
            # Insert the magic bytes at the correct position
            new_request = byte_request[:selection_bounds[0]] + magic_bytes[file_type] + byte_request[selection_bounds[0]:]
            
            # Update the HTTP request
            self._invocation.getSelectedMessages()[0].setRequest(bytes(new_request))
        except Exception as e:
            print("An error occurred while inserting magic bytes: {}".format(str(e)))

