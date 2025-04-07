function openShortVideoUpload() {
    document.getElementById('shortVideoInput').click();
  }

  // Corrected function name and logic
  function uploadShortVideo(input) {
    const file = input.files[0];
    if (file) {
      const fileUrl = URL.createObjectURL(file);
      // Redirect to preview page with video URL as a query parameter
      window.location.href = `/preview?videoUrl=${encodeURIComponent(fileUrl)}`;
    }
  }
  
  function toggleMenu() {
    document.getElementById("menu").classList.toggle("active");
    document.getElementById("overlay").classList.toggle("active");
  }

  function closeMenu() {
    document.getElementById("menu").classList.remove("active");
    document.getElementById("overlay").classList.remove("active");
  }

  function toggleSearch() {
    var searchBar = document.getElementById("search-bar");
    searchBar.classList.toggle("active");
    searchBar.focus();
  }

  const footer = document.getElementById("footer");
  window.addEventListener("resize", () => {
    if (window.innerHeight < 500) {
      footer.classList.add("hidden");
    } else {
      footer.classList.remove("hidden");
    }
  });

  function showPopup() {
    document.getElementById("popup-overlay").style.display = "flex";
  }

  function closePopup() {
    document.getElementById("popup-overlay").style.display = "none";
  }

  document.getElementById("popup-overlay").addEventListener("click", function (event) {
    if (event.target === this) {
      closePopup();
    }
  });

  function toggleUploadMenu() {
    showPopup();
  }
  
function showCommentBox(button) {
    let commentBox = button.nextElementSibling; // अगला डिव (comment-box) ढूंढें
    if (commentBox.style.display === "none") {
      commentBox.style.display = "block";  // दिखाएँ
    } else {
      commentBox.style.display = "none";   // छुपाएँ
    }
  }

  function submitComment(button) {
    let commentBox = button.previousElementSibling; // टेक्स्टएरिया को खोजें
    let content = commentBox.value.trim();  // कॉमेंट का टेक्स्ट लें
    let videoId = "123"; // इसे डायनामिक बनाना होगा

    if (!content) {
      alert("Please write a comment.");
      return;
    }

    fetch('/comment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ video_id: videoId, content: content })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert("Comment added successfully!");
        commentBox.value = ""; // इनपुट साफ करें
      } else {
        alert("Error: " + data.error);
      }
    })
    .catch(error => console.error("Error:", error));
  }