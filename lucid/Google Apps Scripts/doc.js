// event parameter for testing
/*var e = {
  "authMode":"FULL",
  "range":{
    "columnEnd":4,
    "columnStart":4,
    "rowEnd":6,
    "rowStart":6
  },
  "source": SpreadsheetApp.openById('xxxxxxxxxxxxxxxxxxxxx'),
  "triggerUid":"xxxxxxx",
  "user":{
    "email":"xxxxxxx@lucidchart.com",
    "nickname":"name"
  },
  "value":"pass"
};*/

const SHEET_NAME = "Usernames and Passwords";
const DEST_FOLDER_ID = "xxxxxxxxxxx";
const TEMPLATE_FILE_ID = "xxxxxxx";
const TEMPLATE_FIELDS = [ "{{username}}", "{{password}}", "{{hardware}}" ];

/**
 * A trigger-driven function that creates a new user checklist from an existing template, when the password cell is filled.
 *
 * @param {Object} e The event parameter for form submission to a spreadsheet;
 *     see https://developers.google.com/apps-script/understanding_events
 * 
 * Object properties: authMode, oldValue, range, source, triggerUid, user, value
*/
function onPasswordEdit(e) {
  if (e.source.getActiveSheet().getSheetName() == SHEET_NAME) {
    if (e.range.columnStart == 4 && e.range.columnEnd == 4) {
      var startRow = e.range.rowStart;
      var startColumn = e.range.columnStart - 2;
      var numRows = 1;
      var numColumns = 6;
    
      var rowValues = e.source.getSheetValues(startRow, startColumn, numRows, numColumns);
    
      var timestamp = rowValues[0][0];
      var username = rowValues[0][1];
      var password = rowValues[0][2];
      var hardware = rowValues[0][5];
    
      var destFolder = DriveApp.getFolderById(DEST_FOLDER_ID);
      var templateFile = DriveApp.getFileById(TEMPLATE_FILE_ID);
      var newFile = templateFile.makeCopy(username + ' - ' + timestamp, destFolder);
      var body = DocumentApp.openById(newFile.getId()).getBody();
    
      body.replaceText(TEMPLATE_FIELDS[0], username);
      body.replaceText(TEMPLATE_FIELDS[1], password);
      body.replaceText(TEMPLATE_FIELDS[2], hardware);
    }
  }
  //else do nothing, because the password column was not edited
}
