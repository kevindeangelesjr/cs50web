document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-submit').addEventListener('click', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#read-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Use API to query for emails in this mailbox
  fetch(`/emails/${mailbox}`)

  // Convert response to JSON
  .then(response => response.json())


  .then(emails => {

    // Display each email, applying correct css class for read/unread values
    emails.forEach(email => {

      if (email.read) {
        const element = document.createElement('div')
        element.innerHTML = `<div class="read-email"><h4>From: ${email.sender}</h4>Received: ${email.timestamp}<h5>Subject: ${email.subject}</h5></div>`
        element.addEventListener('click', () => display_email(email.id));
        document.querySelector('#emails-view').append(element);

      } else {
        const element = document.createElement('div')
        element.innerHTML = `<div class="unread-email"><h4>From: ${email.sender}</h4>Received: ${email.timestamp}<h5>Subject: ${email.subject}</h5></div>`
        element.addEventListener('click', () => display_email(email.id));
        document.querySelector('#emails-view').append(element);    
      }
    });
  });
}

function send_email() {
  
  // Grab email data from the document
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Post to /email to send the email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })

  // Convert response to JSON
  .then(response => response.json())

  // Check if an error was returned. If so, show an alert.  If not, alert that the email was sent successfully
  .then(response => {

      error_msg = response.error;

      if (error_msg != undefined) {
        alert(`ERROR: ${error_msg}`)
      } else {
        alert('Email sent successfully.')
        load_mailbox('sent');
      }
  });
}

function display_email(email_id) {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#read-view').innerHTML = `<div class="email"><p>Received: ${email.timestamp}</p><h4>${email.sender}</h4><h5>${email.subject}</h5><h6>To: ${email.recipients}</h6><p class="email-body">${email.body}</p></div>`

    console.log(email)

   if (email.archived) {

    const unarchive = document.createElement('div')
    unarchive.innerHTML = '<button class="email-button btn btn-primary">Unarchive</button>'
    unarchive.addEventListener('click', () => unarchive_email(email.id));
    document.querySelector('#read-view').append(unarchive);

   } else {

   const reply = document.createElement('div')
   reply.innerHTML = '<button class="email-button btn btn-primary">Reply</button>'
   reply.addEventListener('click', () => reply_email(email.id));
   document.querySelector('#read-view').append(reply);

   const archive = document.createElement('div')
   archive.innerHTML = '<button class="email-button btn btn-primary">Archive</button>'
   archive.addEventListener('click', () => archive_email(email.id));
   document.querySelector('#read-view').append(archive);
   }

  });
}

function archive_email(email_id) {
  
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })

  location.reload();
}

function unarchive_email(email_id) {

  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })

  location.reload();
}

function reply_email(email_id) {
  
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    const reply_to = email.sender
    const last_time = email.timestamp
    const body = email.body
    let subject = email.subject
    if (!subject.startsWith("re:")) {
      subject = "re: " + subject
    }

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#read-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Set value of composition fields to reflect that it is a reply
    document.querySelector('#compose-recipients').value = `${reply_to}`;
    document.querySelector('#compose-subject').value = `${subject}`;
    document.querySelector('#compose-body').value = `\n\nAt ${last_time}, ${reply_to} wrote: \n\n ${body}`;
});

}