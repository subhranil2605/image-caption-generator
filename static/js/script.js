const clickableDiv = document.getElementById("clickable-div");
const fileInput = document.getElementById("file-input");
const imageFileName = document.getElementById("img-file-name");
const noCaptions = document.getElementsByName("quantity")[0];
const generateCaption = document.getElementById("generate-btn");
const imageUrl = document.getElementsByName("external-url")[0];
const imagePreview = document.getElementById("image-preview");
const testImages = document.getElementsByClassName("test-image");
const generatedCaptions = document.getElementsByClassName("gen-captions")[0];

let file;

let captions;

clickableDiv.addEventListener("click", function () {
  fileInput.click();
});

fileInput.addEventListener("change", function () {
  // show the file name
  file = fileInput.files[0];
  imageFileName.innerHTML = file.name;
});

generateCaption.addEventListener("click", function (event) {
  event.preventDefault();
  deleteH3Elements();
  // console.log(noCaptions.value);
  if (file || imageUrl.value) {
    const formData = new FormData();

    if (file) {
      // preview local image
      previewLocaImage(file);

      formData.append("file", file);
      captionGeneration("http://localhost:5000/upload", formData);
    }
    if (imageUrl.value) {
      imagePreview.src = imageUrl.value;
      formData.append("imgUrl", imageUrl.value.toString());
      captionGeneration("http://localhost:5000/upload", formData);
    }
  } else {
    alert("Select an Image OR Give a URL!!!");
  }
});

for (let i = 0; i < testImages.length; i++) {
  testImages[i].addEventListener("click", function (event) {
    event.preventDefault();
    deleteH3Elements();
    let a = testImages[i].src.toString().replace(/^file:\/\/\//, "");
    imagePreview.src = a;

    // generate captions on predefined test images
    const formData = new FormData();
    formData.append("imgUrl", a);
    captionGeneration("http://localhost:5000/upload", formData);
  });
}

function deleteH3Elements() {
  const container = document.querySelector(".gen-captions");
  const h3Elements = container.querySelectorAll("h3");

  for (let i = 0; i < h3Elements.length; i++) {
    const h3 = h3Elements[i];
    h3.remove();
  }
}

function captionGeneration(url, formData) {
  formData.append("n_capt", noCaptions.value.toString());
  fetch(url, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      captions = data.captions;
      for (let i = 0; i < captions.length; i++) {
        const h3 = document.createElement("h3");
        h3.textContent = captions[i];
        generatedCaptions.appendChild(h3);
      }
    })
    .catch((error) => {
      console.error(error);
    });
}

function previewLocaImage(file) {
  const reader = new FileReader();
  reader.onload = function () {
    imagePreview.src = reader.result;
  };
  reader.readAsDataURL(file);
}
