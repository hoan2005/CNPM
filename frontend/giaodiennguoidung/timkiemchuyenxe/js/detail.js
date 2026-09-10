/**
 * Logic trang Chi tiết chuyến xe & Sơ đồ chọn ghế 2D
 * Xử lý:
 * - Gọi API GET /api/trips/{trip_id}
 * - Gọi API GET /api/trips/{trip_id}/seats
 * - Xử lý ngoại lệ E1: Chuyến xe hết chỗ hoặc bị hủy
 * - Chuyển tầng 1, tầng 2 linh hoạt
 * - Chọn / bỏ chọn ghế và tính tổng tiền tức thì
 */

let currentTrip = null;
let currentSeatMap = null;
let activeFloor = 1;
const selectedSeats = new Map(); // seatCode -> { price, seatType }

document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const tripId = urlParams.get('trip_id') || 1;

    try {
        await loadTripAndSeats(tripId);
    } catch (error) {
        alert(error.message);
        window.location.href = 'index.html';
    }
});

async function loadTripAndSeats(tripId) {
    const [tripDetail, seatMap] = await Promise.all([
        TransLinkAPI.getTripDetail(tripId),
        TransLinkAPI.getSeatMap(tripId)
    ]);

    currentTrip = tripDetail;
    currentSeatMap = seatMap;

    renderTripInfo(tripDetail);
    renderSeatMap(seatMap);
    updatePriceSummary();
}

function renderTripInfo(trip) {
    // Kiểm tra Ngoại lệ E1: Chuyến xe đã bị hủy hoặc hết chỗ
    if (trip.status !== 'active' || trip.available_seats <= 0) {
        const warning = document.getElementById('soldout-warning');
        if (warning) warning.classList.remove('hidden');
    }

    document.getElementById('trip-route-title').textContent = `${trip.departure_point} - ${trip.destination_point}`;
    document.getElementById('trip-date-display').textContent = trip.travel_date;
    document.getElementById('trip-bus-type').textContent = trip.bus_type;
    document.getElementById('trip-operator-name').textContent = trip.operator.name;

    document.getElementById('trip-dep-time').textContent = trip.departure_time;
    document.getElementById('trip-arr-time').textContent = trip.arrival_time;
    document.getElementById('trip-duration-display').textContent = `Thời gian di chuyển dự kiến: ${trip.duration_formatted}`;

    // Điểm đón & trả
    if (trip.pickup_points && trip.pickup_points.length > 0) {
        document.getElementById('trip-dep-point').textContent = trip.pickup_points[0].location;
        document.getElementById('trip-dep-address').textContent = trip.pickup_points[0].address || '';
    } else {
        document.getElementById('trip-dep-point').textContent = trip.departure_point;
    }

    if (trip.dropoff_points && trip.dropoff_points.length > 0) {
        document.getElementById('trip-dest-point').textContent = trip.dropoff_points[0].location;
        document.getElementById('trip-dest-address').textContent = trip.dropoff_points[0].address || '';
    } else {
        document.getElementById('trip-dest-point').textContent = trip.destination_point;
    }

    // Tiện ích
    const amenitiesContainer = document.getElementById('trip-amenities-list');
    if (trip.amenities && trip.amenities.length > 0) {
        amenitiesContainer.innerHTML = trip.amenities.map(a => `
            <div class="flex items-center gap-2 text-text-primary bg-surface-container-lowest px-3 py-1.5 rounded-lg border border-border-default shadow-2xs">
                <span class="material-symbols-outlined text-primary-container text-[18px]">verified</span>
                <span class="font-body-md text-sm">${a}</span>
            </div>
        `).join('');
    } else {
        amenitiesContainer.innerHTML = '<span class="text-secondary text-sm">Tiện ích cơ bản</span>';
    }

    // Chính sách
    const policiesContainer = document.getElementById('trip-policies-list');
    if (trip.policies) {
        const p = trip.policies;
        const items = [];
        if (p.cancellation) items.push(`<li><strong>Hủy vé:</strong> ${p.cancellation}</li>`);
        if (p.baggage) items.push(`<li><strong>Hành lý:</strong> ${p.baggage}</li>`);
        if (p.children) items.push(`<li><strong>Trẻ em:</strong> ${p.children}</li>`);
        if (p.pickup_dropoff) items.push(`<li><strong>Đón/trả:</strong> ${p.pickup_dropoff}</li>`);

        policiesContainer.innerHTML = items.length > 0 ? items.join('') : '<li>Tuân theo quy định chung của nhà xe.</li>';
    }
}

function renderSeatMap(seatMap) {
    const floor2Seats = seatMap.floor_2 || [];
    const floorTabs = document.getElementById('floor-tabs');

    // Nếu không có tầng 2 thì ẩn tab chuyển tầng
    if (floor2Seats.length === 0) {
        floorTabs.classList.add('hidden');
    } else {
        floorTabs.classList.remove('hidden');
    }

    renderFloorSeats(activeFloor);
}

function switchFloor(floorNum) {
    activeFloor = floorNum;
    const btn1 = document.getElementById('btn-floor-1');
    const btn2 = document.getElementById('btn-floor-2');

    if (floorNum === 1) {
        btn1.className = 'px-4 py-2 rounded-lg font-label-sm font-medium bg-primary-container text-white transition-colors';
        btn2.className = 'px-4 py-2 rounded-lg font-label-sm font-medium bg-surface-container text-secondary hover:text-text-primary transition-colors';
    } else {
        btn2.className = 'px-4 py-2 rounded-lg font-label-sm font-medium bg-primary-container text-white transition-colors';
        btn1.className = 'px-4 py-2 rounded-lg font-label-sm font-medium bg-surface-container text-secondary hover:text-text-primary transition-colors';
    }

    renderFloorSeats(floorNum);
}

function renderFloorSeats(floorNum) {
    const container = document.getElementById('seat-grid-container');
    const seats = (floorNum === 1 ? currentSeatMap.floor_1 : currentSeatMap.floor_2) || [];

    if (seats.length === 0) {
        container.innerHTML = '<div class="col-span-3 text-center py-6 text-secondary text-sm">Không có ghế ở tầng này</div>';
        return;
    }

    container.innerHTML = seats.map((seat, index) => {
        const isBooked = seat.status === 'booked';
        const isSelected = selectedSeats.has(seat.seat_code);
        const isVip = seat.seat_type === 'vip';
        const seatPrice = seat.price || currentSeatMap.base_price;

        let statusClass = 'available';
        if (isBooked) statusClass = 'booked';
        else if (isSelected) statusClass = 'selected';
        else if (isVip) statusClass = 'vip';

        // Xếp lối đi giữa nếu chia thành các cột
        return `
            <div 
                onclick="${isBooked ? '' : `toggleSelectSeat('${seat.seat_code}', ${seatPrice}, '${seat.seat_type}')`}"
                class="seat ${statusClass} w-14 h-16 border-2 rounded-t-xl rounded-b-md flex flex-col items-center justify-center font-label-sm text-xs font-semibold shadow-xs"
                title="${seat.seat_code} - ${isBooked ? 'Đã đặt' : new Intl.NumberFormat('vi-VN').format(seatPrice) + 'đ'}"
            >
                <span>${seat.seat_code}</span>
                ${isVip ? '<span class="text-[9px] uppercase tracking-tighter opacity-80">VIP</span>' : ''}
            </div>
        `;
    }).join('');
}

function toggleSelectSeat(seatCode, price, seatType) {
    if (selectedSeats.has(seatCode)) {
        selectedSeats.delete(seatCode);
    } else {
        selectedSeats.set(seatCode, { price, seatType });
    }

    renderFloorSeats(activeFloor);
    updatePriceSummary();
}

function updatePriceSummary() {
    const countElem = document.getElementById('selected-seats-count');
    const listElem = document.getElementById('selected-seats-list');
    const basePriceElem = document.getElementById('summary-base-price');
    const totalElem = document.getElementById('summary-total-price');
    const btnCheckout = document.getElementById('btn-continue-checkout');

    const basePrice = currentSeatMap ? currentSeatMap.base_price : 0;
    basePriceElem.textContent = `${new Intl.NumberFormat('vi-VN').format(basePrice)} đ`;

    const count = selectedSeats.size;
    countElem.textContent = count;

    if (count === 0) {
        listElem.textContent = 'Chưa chọn';
        totalElem.textContent = '0 đ';
        if (btnCheckout) btnCheckout.disabled = true;
        return;
    }

    const seatCodes = Array.from(selectedSeats.keys());
    listElem.textContent = seatCodes.join(', ');

    let total = 0;
    selectedSeats.forEach(item => {
        total += item.price;
    });

    totalElem.textContent = `${new Intl.NumberFormat('vi-VN').format(total)} đ`;
    if (btnCheckout) btnCheckout.disabled = false;
}

function handleContinueBooking() {
    if (selectedSeats.size === 0) {
        alert('Vui lòng chọn ít nhất 1 chỗ ngồi!');
        return;
    }
    const seatCodes = Array.from(selectedSeats.keys()).join(',');
    alert(`Bạn đã chọn thành công ghế: [${seatCodes}]. Tiến hành chuyển sang bước 3 (Nhập thông tin khách hàng)!`);
}
