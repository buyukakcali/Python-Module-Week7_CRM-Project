// Recursive function to remove sharing permissions
function removeFolderSharing(folder) {
  try {
    // Logger.log('Processing folder: ' + folder.getName());

    var editors = folder.getEditors();
    var viewers = folder.getViewers();

    // Remove public sharing if it's shared with anyone with the link
    if (folder.getSharingAccess() === DriveApp.Access.ANYONE_WITH_LINK) {
      folder.setSharing(DriveApp.Access.PRIVATE, DriveApp.Permission.NONE);
      Logger.log('Sharing with anyone with the link removed for folder: ' + folder.getName());
    }

    // Remove editors
    for (var i = 0; i < editors.length; i++) {
      folder.removeEditor(editors[i]);
      Logger.log('Editor removed from folder: ' + folder.getName() + ', Editor: ' + editors[i].getEmail());
    }

    // Remove viewers
    for (var j = 0; j < viewers.length; j++) {
      folder.removeViewer(viewers[j]);
      Logger.log('Viewer removed from folder: ' + folder.getName() + ', Viewer: ' + viewers[j].getEmail());
    }

    // Recursively process all subfolders
    var subFolders = folder.getFolders();
    while (subFolders.hasNext()) {
      var subFolder = subFolders.next();
      removeFolderSharing(subFolder);  // Recursive call for each subfolder
    }
  } catch (e) {
    console.error('Error occurred in removeFolderSharing function: ' + e.stack);
  }
}
