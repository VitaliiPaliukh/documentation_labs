(function () {
    var trigger = document.getElementById("admin-secret-trigger");
    var modal = document.getElementById("admin-unlock-modal");
    var form = document.getElementById("admin-unlock-form");
    var cancelButton = document.getElementById("admin-unlock-cancel");
    var errorField = document.getElementById("admin-unlock-error");
    var dimmer = document.getElementById("failed-login-dimmer");
    var clickCount = 0;
    var lastClickAt = 0;
    var darkLevel = 0;

    if (!trigger || !modal || !form || !window.adminUnlockConfig) {
        return;
    }

    function setModalVisible(isVisible) {
        if (isVisible) {
            modal.classList.add("visible");
            modal.setAttribute("aria-hidden", "false");
            document.getElementById("admin-login").focus();
            return;
        }

        modal.classList.remove("visible");
        modal.setAttribute("aria-hidden", "true");
        form.reset();
        errorField.textContent = "";
    }

    function darkenScreen() {
        darkLevel = Math.min(darkLevel + 0.2, 0.9);
        dimmer.classList.add("active");
        dimmer.style.background = "rgba(0, 0, 0, " + darkLevel.toFixed(2) + ")";
    }

    trigger.addEventListener("click", function () {
        var now = Date.now();
        if (now - lastClickAt > 1200) {
            clickCount = 0;
        }

        clickCount += 1;
        lastClickAt = now;

        if (clickCount >= 3) {
            clickCount = 0;
            setModalVisible(true);
        }
    });

    cancelButton.addEventListener("click", function () {
        setModalVisible(false);
    });

    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            setModalVisible(false);
        }
    });

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        var login = document.getElementById("admin-login").value.trim();
        var password = document.getElementById("admin-password").value;

        fetch(window.adminUnlockConfig.unlockUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ login: login, password: password })
        })
            .then(function (response) {
                if (response.ok) {
                    window.location.reload();
                    return;
                }

                darkenScreen();
                return response.json().then(function (payload) {
                    errorField.textContent = payload.message || "Unlock failed.";
                });
            })
            .catch(function () {
                darkenScreen();
                errorField.textContent = "Server error. Try again.";
            });
    });
})();

