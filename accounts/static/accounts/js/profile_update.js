const imageInput = document.getElementById(
        "{{ form.profile_image.id_for_label }}"
    );

    const uploadPreview = document.getElementById("uploadPreview");

    const profilePreview = document.getElementById("profilePreview");


    if (imageInput) {

        imageInput.addEventListener("change", function () {

            const file = this.files[0];

            if (file) {

                const reader = new FileReader();

                reader.onload = function (e) {

                    // Update upload preview
                    if (uploadPreview) {

                        if (uploadPreview.tagName === "IMG") {
                            uploadPreview.src = e.target.result;
                        } else {

                            const img = document.createElement("img");

                            img.src = e.target.result;
                            img.alt = "Profile Preview";
                            img.id = "uploadPreview";

                            uploadPreview.replaceWith(img);

                        }

                    }


                    // Update main profile preview
                    if (profilePreview) {

                        if (profilePreview.tagName === "IMG") {
                            profilePreview.src = e.target.result;
                        } else {

                            const img = document.createElement("img");

                            img.src = e.target.result;
                            img.alt = "Profile Preview";
                            img.id = "profilePreview";
                            img.className = "profile-image";

                            profilePreview.replaceWith(img);

                        }

                    }

                };

                reader.readAsDataURL(file);

            }

        });

    }