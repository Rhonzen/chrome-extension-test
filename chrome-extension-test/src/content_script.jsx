import React from 'react';
import { createRoot } from 'react-dom/client';

// Observes any changes on the twitter timeline
// (changes to number of tweets from scrolling)
const observer = new MutationObserver(() => {
  const tweetList = document.querySelectorAll('[data-testid="tweet"]');

  // Waits for at least 1 tweet to appear
  if (tweetList.length > 0) {
    tweetList.forEach(createButton);
  }
})
observer.observe(document.body, {childList: true, subtree: true});

// Blue analyse button
function AnalyseButton({ onClick }) {
  return (
    <div>
      <button className='analyse-button' onClick={onClick}>
        analyse
      </button>
    </div>
  );
}

// Container for claims, evidence and analysis
function ClaimsBox(claims) {
  return (
    <div className='claims-box'>
      {claims.map((claim, index) => (
        <div key={index}  className='claim-container'>
          <hr></hr>
          <h1 className='claim-header'>Claim: {claim.claim}</h1>
          <div className='analysis'>{claim.analysis}</div>
        </div>
      ))}
    </div>
  );
}

// Appends a button to the end of the tweet's text
function createButton(tweet) {
  let tweetText = tweet.querySelector('[data-testid="tweetText"]');

  // Skips tweets that have no text
  if (!tweetText || !tweetText.querySelector('span')) {
    return;
  }
  // Skips tweets that already have a button
  else if (tweet.querySelector('.checked')) {
    return;
  }

  // Creates a POST request to the flask backend
  const analyseText = () => {
    const tweetTextContent = tweetText.querySelector('span').innerHTML;
    const tweetJson = {tweet_text: tweetTextContent};

    // Sends the tweet's text content for analysis
    fetch('http://localhost:1000/analyse', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(tweetJson),
    })
    .then(response => response.json())
    // Successful analysis
    .then(data => {
      // Creates a box for claims
      const claimDomNode = document.createElement('div');
      const claimRoot = createRoot(claimDomNode);
      claimRoot.render(ClaimsBox(data));
      tweet.insertAdjacentElement('afterend', claimDomNode);

      // Outlines the post (red, orange, green) depending on its accuracy
      const accuracy = getAccuracy(data);
      tweet.style.border = `2px solid ${accuracy}`;

      // Hides analysis button
      domNode.classList.add('hide');
    })
    // Failed analysis
    .catch(error => {
      console.error('Error:', error);
    });
  };
  
  // Creates and appends an 'analyse' button to the tweet's text
  const domNode = document.createElement('div');
  domNode.classList.add('checked');
  const root = createRoot(domNode);
  root.render(<AnalyseButton onClick={analyseText} />);
  tweetText.appendChild(domNode);
}

// Estimates the overall accuracy of the post
function getAccuracy(claims) {
  let accuracy = 0;
  let highCount = 0;
  let lowCount = 0;
  let mediumCount = 0;
  claims.forEach((claim) => {
    if (claim.accuracy === 'high') {
      accuracy++;
      highCount++;
    }
    else if (claim.accuracy === 'medium') {
      mediumCount++;
    }
    else if (claim.accuracy === 'low') {
      accuracy--;
      lowCount++;
    }
  });

  if (accuracy === 0 || mediumCount > 2) {
    console.log('orange');
    return 'orange';
  }
  else if (lowCount === 0) {
    console.log('green');
    return 'green';
  }
  else if (highCount === 0) {
    return 'red';
  }
  return 'orange';
}