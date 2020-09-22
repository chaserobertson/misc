
// definition of test response object e
/*var surveyResponses = ['7/13/2020 11:55:16',
                       'John',
                       'Doe',
                       '801-911-9111',
                       'SOJO',
                       'Full-Time',
                       'Black Ops',
                       'Black Ops (AMS)',
                       'Chromebook',
                       '12/30/1970',
                       '12/31/1970',
                       'No comments or questions'
                      ];
var e = {
  namedValues: {},
  values: []
 };
for (i=0; i<surveyQuestions.length; i++) {
  e.namedValues[surveyQuestions[i]] = surveyResponses[i];
  e.values[i] = surveyResponses[i];
}*/

/**
 * A trigger-driven function that sends out several ticket creation emails after a user responds to the form.
 *
 * @param {Object} e The event parameter for form submission to a spreadsheet;
 *     see https://developers.google.com/apps-script/understanding_events
 */
function onFormSubmit(e) {

  const recipientEmail = "xxxxx@lucidchart.com";
  const ccEmail = "xxxxxx@lucidchart.com";
  const replyToEmail = "xxxxx@lucidchart.com";
  const year = "2020";
  const numEmails = 3;
  const surveyQuestions = [
    'Timestamp',
    'What first name would you like to go by at Lucid?',
    'What last name would you like to go by at Lucid?',
    'What is your cell phone number?',
    'What office will you be working at?',
    'What will your employment status be?',
    'What department will you be in?',
    'What department will you be in? (Amsterdam Office)',
    'Which laptop do you prefer?',
    'Projected Start Date',
    'Projected End Date',
    'Comments/Questions'
  ];
  const defaultEmailBodies = [
    "#tags employee_onboard\n" +
    "0. Update the ticket subject with the correct start date.\n\n" +
    "1. Open - accounts.lucidauth.com, IT New Hire spreadsheet, PeopleOps New Hire spreadsheet.\n\n" +
    "2. Paste data from IT New Hire (Usernames and Passwords) to accounts.lucidauth.com to create new account. Verify data and groups with the country sheet and manager info.\n\n" +
    "3. Paste new credentials into \"Usernames and Passwords\", then paste the email address into this ticket and close out.\n\n",

    "#tags employee_onboard\n" +
    "0. Update the ticket subject with the correct start date.\n\n" +
    "1. Print a new hire setup checklist from https://drive.google.com/drive/u/0/folders/xxxxxx\n\n" +
    "2. Provision a laptop using that user's info.\n\n" +
    "3. Record the completion of provisioning in the appropriate column of the New Hire Info spreadsheet: https://docs.google.com/spreadsheets/d/xxxxxxx\n\n",

    "#tags employee_onboard\n" +
    "0. Update the ticket subject with the correct start date.\n\n" + 
    "1. Check the New Hire Info spreadsheet for shipping/pickup information https://docs.google.com/spreadsheets/d/xxxxx\n\n" +
    "2a. If laptop needs to be shipped, refer to this document for directions https://lucidsoftware.zendesk.com/hc/en-us/articles/xxxxxx\n" +
    "2b. If laptop will be picked up, attend the scheduled pickup calendar event to hand out the laptop.\n\n"
  ];

  var userFullName = e.namedValues[surveyQuestions[1]] + ' ' + e.namedValues[surveyQuestions[2]];
  var generalEmailSubject = year + '-00-00 - ' + userFullName + ' - ';

  var emailSubjects = [];
  emailSubjects[0] = generalEmailSubject + 'Account Setup';
  emailSubjects[1] = generalEmailSubject + 'Laptop Setup';
  emailSubjects[2] = generalEmailSubject + 'Laptop Pickup/Ship';

  var responseValues = "";
  for (const x in surveyQuestions) {
    if (e.values[x] != "") {
      responseValues += e.values[x] + "\n";
    }
  }
  
  var emailBodies = [];
  for (body in defaultEmailBodies) {
    emailBodies[i] = defaultEmailBodies[i] + responseValues;
  }
  
  for (i=0; i<numEmails; i++) {
    var emailObject = {
      to: recipientEmail,
      replyTo: replyToEmail,
      subject: emailSubjects[i],
      body: emailBodies[i]
    };
    
    if (i == 0) emailObject["cc"] = ccEmail;
      
    MailApp.sendEmail(emailObject);
  }
}