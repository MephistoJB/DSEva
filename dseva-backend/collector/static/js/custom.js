// Initialisiert die Anzeige für das Rate Limit
function initRateLimitMonitor() {
    const eventSource = new EventSource("/infos/ratelimit");

    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log("Rate Limit Info:", data);

        const $badge = $("#ratelimit-badge");
        if ($badge.length) {
            $badge.text(`${data.remaining} remaining / ${data.buffer} buffer`);
            $badge.removeClass("bg-danger bg-warning bg-success");

            if (data.remaining > 1000) {
                $badge.addClass("bg-success");
            } else if (data.remaining > 100) {
                $badge.addClass("bg-warning");
            } else {
                $badge.addClass("bg-danger");
            }
        }
    };

    eventSource.onerror = function(err) {
        console.error("SSE error:", err);
    };
}

// Holt aktuellen Zustand des Verarbeitungs-Buttons vom Server
function updateProcessingButton() {
    $.get('/process', function(data) {
        $('#toggle-processing-btn').text(data.processing_enabled ? 'Stop' : 'Start');
    });
}

// Event-Handler für den Klick auf den Verarbeitungs-Button
function setup() {
    $('#toggle-processing-btn').on('click', function() {
        const newState = $(this).text() === 'Start';
        $.ajax({
            url: '/process',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ enabled: newState }),
            success: function() {
                updateProcessingButton();
            },
            error: function() {
                $('#toastErrorMessage').text('Failed to toggle processing.');
                $('#toastError').toast('show');
            }
        });
    });

    // Initialisiere den EventSource für den Running-Status
    const runningStatusSource = new EventSource("/infos/running");
    runningStatusSource.onmessage = function(event) {
        const status = JSON.parse(event.data);
        console.log("Running Status:", status);

        const $statusBadge = $('#status');
        if ($statusBadge.length) {
            if (status.running) {
                $statusBadge
                    .removeClass('bg-danger')
                    .addClass('bg-success')
                    .text('Running');
            } else {
                $statusBadge
                    .removeClass('bg-success')
                    .addClass('bg-danger')
                    .text('Not Running');
            }
        }
    };

    // Initialisiere den EventSource für die nächsten Elemente
    const nextElementsSource = new EventSource("/infos/nextelements");
    nextElementsSource.onmessage = function(event) {
        const elements = JSON.parse(event.data);
        console.log("Next Elements:", elements);
        const $list = $('#next-elements-list');
        $list.empty(); // Vorherige Einträge entfernen
        elements.forEach(function(element) {
            $list.append(`<li class="list-group-item">${element}</li>`);
        });
    };
}

// Initialisierung beim Laden des Dokuments
$(document).ready(function() {
    updateProcessingButton();
    initRateLimitMonitor();
    setup();
});