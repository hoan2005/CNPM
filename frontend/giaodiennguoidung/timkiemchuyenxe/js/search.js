/**
 * Logic tìm kiếm, lọc và hiển thị danh sách chuyến xe
 * Xử lý đầy đủ:
 * - Ngoại lệ E1: Điểm đi == Điểm đến -> Thông báo lỗi
 * - Luồng thay thế A1: Mặc định ngày hôm nay nếu chưa chọn
 * - Ngoại lệ E2: Không có chuyến xe -> Hiển thị Empty state
 * - Bộ lọc: Giờ, Loại xe, Khoảng giá, Nhà xe
 * - Điều hướng: Sang trip-detail.html?trip_id=...
 */

// Danh mục các tỉnh thành tại Việt Nam phục vụ chọn điểm đi & điểm đến
const VIETNAM_PROVINCES = [
    { name: "Đà Nẵng", region: "Miền Trung", popular: true },
    { name: "Huế", region: "Miền Trung", popular: true },
    { name: "Hà Nội", region: "Miền Bắc", popular: true },
    { name: "Hồ Chí Minh", region: "Miền Nam", popular: true },
    { name: "Nha Trang", region: "Miền Trung", popular: true },
    { name: "Đà Lạt", region: "Tây Nguyên", popular: true },
    { name: "Cần Thơ", region: "Miền Nam", popular: true },
    { name: "Vũng Tàu", region: "Miền Nam", popular: true },
    { name: "Hải Phòng", region: "Miền Bắc", popular: true },
    { name: "Quy Nhơn", region: "Miền Trung", popular: true },
    { name: "Quảng Ngãi", region: "Miền Trung", popular: true },
    { name: "Quảng Nam", region: "Miền Trung", popular: true },
    { name: "Phan Thiết", region: "Miền Trung", popular: false },
    { name: "Buôn Ma Thuột", region: "Tây Nguyên", popular: false },
    { name: "Pleiku", region: "Tây Nguyên", popular: false },
    { name: "Kon Tum", region: "Tây Nguyên", popular: false },
    { name: "Quảng Bình", region: "Miền Trung", popular: false },
    { name: "Quảng Trị", region: "Miền Trung", popular: false },
    { name: "Hà Tĩnh", region: "Miền Trung", popular: false },
    { name: "Nghệ An", region: "Miền Trung", popular: false },
    { name: "Thanh Hóa", region: "Miền Trung", popular: false },
    { name: "Ninh Bình", region: "Miền Bắc", popular: false },
    { name: "Nam Định", region: "Miền Bắc", popular: false },
    { name: "Thái Bình", region: "Miền Bắc", popular: false },
    { name: "Hải Dương", region: "Miền Bắc", popular: false },
    { name: "Hưng Yên", region: "Miền Bắc", popular: false },
    { name: "Bắc Ninh", region: "Miền Bắc", popular: false },
    { name: "Bắc Giang", region: "Miền Bắc", popular: false },
    { name: "Quảng Ninh", region: "Miền Bắc", popular: false },
    { name: "Lạng Sơn", region: "Miền Bắc", popular: false },
    { name: "Thái Nguyên", region: "Miền Bắc", popular: false },
    { name: "Phú Thọ", region: "Miền Bắc", popular: false },
    { name: "Vĩnh Phúc", region: "Miền Bắc", popular: false },
    { name: "Lào Cai (Sa Pa)", region: "Miền Bắc", popular: false },
    { name: "Yên Bái", region: "Miền Bắc", popular: false },
    { name: "Hòa Bình", region: "Miền Bắc", popular: false },
    { name: "Sơn La", region: "Miền Bắc", popular: false },
    { name: "Điện Biên", region: "Miền Bắc", popular: false },
    { name: "Lai Châu", region: "Miền Bắc", popular: false },
    { name: "Hà Giang", region: "Miền Bắc", popular: false },
    { name: "Cao Bằng", region: "Miền Bắc", popular: false },
    { name: "Bắc Kạn", region: "Miền Bắc", popular: false },
    { name: "Tuyên Quang", region: "Miền Bắc", popular: false },
    { name: "Phú Yên", region: "Miền Trung", popular: false },
    { name: "Ninh Thuận", region: "Miền Trung", popular: false },
    { name: "Bình Thuận", region: "Miền Trung", popular: false },
    { name: "Đắk Lắk", region: "Tây Nguyên", popular: false },
    { name: "Đắk Nông", region: "Tây Nguyên", popular: false },
    { name: "Gia Lai", region: "Tây Nguyên", popular: false },
    { name: "Lâm Đồng", region: "Tây Nguyên", popular: false },
    { name: "Bình Phước", region: "Miền Nam", popular: false },
    { name: "Bình Dương", region: "Miền Nam", popular: false },
    { name: "Đồng Nai", region: "Miền Nam", popular: false },
    { name: "Tây Ninh", region: "Miền Nam", popular: false },
    { name: "Bà Rịa - Vũng Tàu", region: "Miền Nam", popular: false },
    { name: "Long An", region: "Miền Nam", popular: false },
    { name: "Tiền Giang", region: "Miền Nam", popular: false },
    { name: "Bến Tre", region: "Miền Nam", popular: false },
    { name: "Trà Vinh", region: "Miền Nam", popular: false },
    { name: "Vĩnh Long", region: "Miền Nam", popular: false },
    { name: "Đồng Tháp", region: "Miền Nam", popular: false },
    { name: "An Giang", region: "Miền Nam", popular: false },
    { name: "Kiên Giang", region: "Miền Nam", popular: false },
    { name: "Hậu Giang", region: "Miền Nam", popular: false },
    { name: "Sóc Trăng", region: "Miền Nam", popular: false },
    { name: "Bạc Liêu", region: "Miền Nam", popular: false },
    { name: "Cà Mau", region: "Miền Nam", popular: false }
];

document.addEventListener('DOMContentLoaded', () => {
    // Gán ngày hôm nay mặc định cho input ngày nếu chưa có
    const dateInput = document.getElementById('search-date');
    if (!dateInput.value) {
        const todayStr = new Date().toISOString().split('T')[0];
        dateInput.value = todayStr;
    }

    // Khởi tạo bộ chọn địa điểm (Dropdown & Autocomplete)
    initLocationPickers();

    // Tự động tìm kiếm lần đầu khi tải trang
    executeSearch();
});

// Loại bỏ dấu tiếng Việt để tìm kiếm không dấu
function removeVietnameseTones(str) {
    if (!str) return '';
    str = str.toLowerCase();
    str = str.replace(/à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ/g, "a");
    str = str.replace(/è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ/g, "e");
    str = str.replace(/ì|í|ị|ỉ|ĩ/g, "i");
    str = str.replace(/ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ/g, "o");
    str = str.replace(/ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ/g, "u");
    str = str.replace(/ỳ|ý|ỵ|ỷ|ỹ/g, "y");
    str = str.replace(/đ/g, "d");
    return str.trim();
}

/**
 * Khởi tạo sự kiện cho các ô Điểm đi và Điểm đến
 */
function initLocationPickers() {
    ['departure', 'destination'].forEach(type => {
        const input = document.getElementById(`search-${type}`);
        const dropdown = document.getElementById(`dropdown-${type}`);
        if (!input) return;

        if (dropdown) {
            dropdown.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        }

        // Khi người dùng click hoặc focus vào ô input
        input.addEventListener('focus', () => {
            renderLocationDropdown(type, input.value.trim());
            openLocationDropdown(type);
        });

        input.addEventListener('click', (e) => {
            e.stopPropagation();
            renderLocationDropdown(type, input.value.trim());
            openLocationDropdown(type);
        });

        // Khi người dùng gõ phím để tìm kiếm (Autocomplete)
        input.addEventListener('input', (e) => {
            renderLocationDropdown(type, e.target.value.trim());
            openLocationDropdown(type);
        });

        // Hỗ trợ phím Enter (chọn kết quả đầu tiên) và Escape (đóng)
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const firstItem = dropdown ? dropdown.querySelector('.location-item') : null;
                if (firstItem) {
                    const locName = firstItem.getAttribute('data-location-name');
                    if (locName) selectLocation(type, locName);
                } else {
                    closeLocationDropdown(type);
                    executeSearch();
                }
            } else if (e.key === 'Escape') {
                closeLocationDropdown(type);
            }
        });
    });

    // Đóng dropdown khi click ra ngoài
    document.addEventListener('click', (e) => {
        ['departure', 'destination'].forEach(type => {
            const wrapper = document.getElementById(`wrapper-${type}`);
            if (wrapper && !wrapper.contains(e.target)) {
                closeLocationDropdown(type);
            }
        });
    });
}

function openLocationDropdown(type) {
    const dropdown = document.getElementById(`dropdown-${type}`);
    const arrow = document.getElementById(`arrow-${type}`);
    const otherType = type === 'departure' ? 'destination' : 'departure';
    
    // Đóng dropdown còn lại
    closeLocationDropdown(otherType);

    if (dropdown) {
        dropdown.classList.remove('hidden');
    }
    if (arrow) {
        arrow.classList.add('rotate-180');
    }
}

function closeLocationDropdown(type) {
    const dropdown = document.getElementById(`dropdown-${type}`);
    const arrow = document.getElementById(`arrow-${type}`);
    if (dropdown) {
        dropdown.classList.add('hidden');
    }
    if (arrow) {
        arrow.classList.remove('rotate-180');
    }
}

function toggleLocationDropdown(type, event) {
    if (event) event.stopPropagation();
    const dropdown = document.getElementById(`dropdown-${type}`);
    if (dropdown && !dropdown.classList.contains('hidden')) {
        closeLocationDropdown(type);
    } else {
        const input = document.getElementById(`search-${type}`);
        renderLocationDropdown(type, input ? input.value.trim() : '');
        openLocationDropdown(type);
    }
}

function renderLocationDropdown(type, filterText = '') {
    const dropdown = document.getElementById(`dropdown-${type}`);
    if (!dropdown) return;

    const normalizedFilter = removeVietnameseTones(filterText);
    
    // Lọc danh sách theo từ khóa
    const filteredList = VIETNAM_PROVINCES.filter(item => {
        if (!normalizedFilter) return true;
        const normalizedName = removeVietnameseTones(item.name);
        const normalizedRegion = removeVietnameseTones(item.region);
        return normalizedName.includes(normalizedFilter) || normalizedRegion.includes(normalizedFilter);
    });

    const popularList = VIETNAM_PROVINCES.filter(item => item.popular);

    let html = '';

    // Nếu không gõ bộ lọc (hoặc bộ lọc rỗng), hiện mục "Địa điểm phổ biến"
    if (!normalizedFilter) {
        html += `
        <div class="mb-3 pb-2.5 border-b border-border-default">
            <div class="text-[11px] font-semibold uppercase tracking-wider text-secondary mb-2 flex items-center gap-1">
                <span class="material-symbols-outlined text-[15px] text-primary">local_fire_department</span>
                <span>Địa điểm phổ biến</span>
            </div>
            <div class="flex flex-wrap gap-1.5">
                ${popularList.map(item => `
                    <button type="button" onclick="selectLocation('${type}', '${item.name}')" class="text-xs bg-surface-container hover:bg-primary-container hover:text-white px-2.5 py-1 rounded-full transition-colors font-medium">
                        ${item.name}
                    </button>
                `).join('')}
            </div>
        </div>
        `;
    }

    // Danh sách các địa điểm
    html += `
    <div class="text-[11px] font-semibold uppercase tracking-wider text-secondary mb-1.5 flex items-center justify-between">
        <span>${normalizedFilter ? `Kết quả tìm kiếm (${filteredList.length})` : 'Tất cả tỉnh thành'}</span>
    </div>
    `;

    if (filteredList.length === 0) {
        html += `
        <div class="py-6 text-center text-secondary">
            <span class="material-symbols-outlined text-3xl mb-1 text-outline">search_off</span>
            <p class="text-xs">Không tìm thấy tỉnh thành "${filterText}"</p>
        </div>
        `;
    } else {
        html += `<div class="space-y-0.5 max-h-52 overflow-y-auto custom-scrollbar pr-1">`;
        filteredList.forEach(item => {
            html += `
            <div onclick="selectLocation('${type}', '${item.name}')" data-location-name="${item.name}" class="location-item flex items-center justify-between px-2.5 py-2 rounded-lg hover:bg-surface-container cursor-pointer transition-colors group">
                <div class="flex items-center gap-2">
                    <span class="material-symbols-outlined text-[18px] text-secondary group-hover:text-primary transition-colors">location_on</span>
                    <span class="font-body-md text-body-md text-text-primary group-hover:text-primary font-medium">${item.name}</span>
                </div>
                <span class="text-[11px] text-secondary bg-surface-container-high group-hover:bg-primary-fixed group-hover:text-primary px-2 py-0.5 rounded-full transition-colors">${item.region}</span>
            </div>
            `;
        });
        html += `</div>`;
    }

    dropdown.innerHTML = html;
}

function selectLocation(type, locationName) {
    const input = document.getElementById(`search-${type}`);
    if (input) {
        input.value = locationName;
    }
    closeLocationDropdown(type);
    hideErrorAlert();
}

/**
 * Nút hoán đổi Điểm đi <-> Điểm đến
 */
function handleSwapLocations() {
    const depInput = document.getElementById('search-departure');
    const destInput = document.getElementById('search-destination');
    if (!depInput || !destInput) return;

    const temp = depInput.value;
    depInput.value = destInput.value;
    destInput.value = temp;

    hideErrorAlert();
    executeSearch();
}

function showErrorAlert(message) {
    const alertBox = document.getElementById('error-alert');
    const msgElem = document.getElementById('error-message');
    msgElem.textContent = message;
    alertBox.classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function hideErrorAlert() {
    const alertBox = document.getElementById('error-alert');
    alertBox.classList.add('hidden');
}

function handlePriceSlider(value) {
    const formatted = new Intl.NumberFormat('vi-VN').format(value);
    document.getElementById('price-slider-display').textContent = `Dưới ${formatted}đ`;
}

function handleSearchClick() {
    executeSearch();
}

function handleResetFilters() {
    // Reset radio giờ
    const firstTimeRadio = document.querySelector('input[name="time_slot"][value=""]');
    if (firstTimeRadio) firstTimeRadio.checked = true;

    // Reset loại xe
    document.querySelectorAll('.filter-bus-type').forEach(cb => cb.checked = false);

    // Reset nhà xe
    document.querySelectorAll('.filter-operator').forEach(cb => cb.checked = false);

    // Reset slider giá
    const slider = document.getElementById('price-slider');
    slider.value = 500000;
    handlePriceSlider(500000);

    // Reset sort
    document.getElementById('sort-select').value = 'departure_time-asc';

    // Thực hiện lại tìm kiếm
    executeSearch();
}

function applyFilters() {
    executeSearch();
}

async function executeSearch() {
    hideErrorAlert();

    const departure = document.getElementById('search-departure').value.trim();
    const destination = document.getElementById('search-destination').value.trim();
    const travelDate = document.getElementById('search-date').value;
    const passengers = document.getElementById('search-passengers').value;

    // Kiểm tra client-side trước cho ngoại lệ E1 (Điểm đi = Điểm đến)
    if (departure && destination && departure.toLowerCase() === destination.toLowerCase()) {
        showErrorAlert('Điểm đi và điểm đến không được trùng nhau');
        renderEmptyState(true);
        return;
    }

    // Thu thập các bộ lọc
    const timeSlotRadio = document.querySelector('input[name="time_slot"]:checked');
    const timeSlot = timeSlotRadio ? timeSlotRadio.value : '';

    const busTypes = [];
    document.querySelectorAll('.filter-bus-type:checked').forEach(cb => busTypes.push(cb.value));

    const operators = [];
    document.querySelectorAll('.filter-operator:checked').forEach(cb => operators.push(cb.value));

    const maxPrice = document.getElementById('price-slider').value;

    // Phân tích sort
    const sortVal = document.getElementById('sort-select').value;
    const [sortBy, sortOrder] = sortVal.split('-');

    const params = {
        departure,
        destination,
        travelDate,
        passengers,
        maxPrice,
        timeSlot: timeSlot || undefined,
        busTypes: busTypes.length > 0 ? busTypes : undefined,
        operators: operators.length > 0 ? operators : undefined,
        sortBy,
        sortOrder
    };

    try {
        const data = await TransLinkAPI.searchTrips(params);
        renderTrips(data.trips);
    } catch (error) {
        showErrorAlert(error.message);
        renderEmptyState(true);
    }
}

function renderTrips(trips) {
    const container = document.getElementById('trips-container');
    const emptyState = document.getElementById('empty-state');
    const totalCount = document.getElementById('total-trips-count');

    totalCount.textContent = trips.length;

    if (!trips || trips.length === 0) {
        renderEmptyState(false);
        return;
    }

    emptyState.classList.add('hidden');
    container.classList.remove('hidden');

    container.innerHTML = trips.map(trip => {
        const isSoldOut = trip.available_seats <= 0 || trip.status !== 'active';
        const formattedPrice = new Intl.NumberFormat('vi-VN').format(trip.price) + 'đ';

        // Ảnh logo nhà xe
        const logoUrl = trip.operator.logo_url || 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=100&h=100&fit=crop';

        return `
        <article class="bg-surface-container-lowest rounded-xl shadow-sm border border-border-default p-stack-md flex flex-col sm:flex-row items-start sm:items-center justify-between gap-stack-md hover:shadow-md transition-shadow">
            <div class="flex items-start space-x-4 flex-1">
                <div class="w-16 h-16 rounded-lg bg-surface-container-low flex items-center justify-center overflow-hidden flex-shrink-0 p-1 border border-border-default">
                    <img class="w-full h-full object-contain" src="${logoUrl}" alt="${trip.operator.name}" onerror="this.src='https://cdn-icons-png.flaticon.com/512/3448/3448339.png'"/>
                </div>
                <div class="flex-1">
                    <h3 class="font-headline-h3 text-headline-h3 text-text-primary mb-1">${trip.operator.name}</h3>
                    <div class="flex items-center space-x-2 font-caption text-caption text-secondary mb-2">
                        <span class="bg-surface-container py-1 px-2 rounded-full font-medium">${trip.bus_type}</span>
                        <span class="flex items-center text-warning"><span class="material-symbols-outlined text-[16px] mr-0.5">star</span> <span class="text-text-primary font-medium">${trip.rating}</span> <span class="text-secondary ml-1">(${trip.review_count || 100})</span></span>
                    </div>
                    <div class="flex items-center space-x-4 mt-3">
                        <div class="text-center">
                            <div class="font-headline-h3 text-headline-h3 ${isSoldOut ? 'text-text-muted' : 'text-text-primary'}">${trip.departure_time}</div>
                            <div class="font-caption text-caption text-secondary">${trip.departure_point}</div>
                        </div>
                        <div class="flex-1 flex flex-col items-center px-4 relative max-w-[120px]">
                            <div class="font-caption text-caption text-text-muted mb-1">${trip.duration_formatted}</div>
                            <div class="w-full h-[2px] bg-border-default relative">
                                <div class="absolute left-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full ${isSoldOut ? 'bg-text-muted' : 'bg-primary-container'}"></div>
                                <div class="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-outline"></div>
                            </div>
                        </div>
                        <div class="text-center">
                            <div class="font-headline-h3 text-headline-h3 ${isSoldOut ? 'text-text-muted' : 'text-text-primary'}">${trip.arrival_time}</div>
                            <div class="font-caption text-caption text-secondary">${trip.destination_point}</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="flex flex-row sm:flex-col items-center sm:items-end justify-between w-full sm:w-auto border-t sm:border-t-0 sm:border-l border-border-default pt-4 sm:pt-0 sm:pl-stack-md mt-4 sm:mt-0 ${isSoldOut ? 'opacity-75' : ''}">
                <div class="text-left sm:text-right mb-0 sm:mb-4">
                    <div class="font-headline-h2 text-headline-h2 ${isSoldOut ? 'text-text-muted' : 'text-primary-container'} font-bold">${formattedPrice}</div>
                    ${isSoldOut 
                        ? `<div class="font-caption text-caption text-error flex items-center justify-start sm:justify-end mt-1">
                                <span class="material-symbols-outlined text-[14px] mr-1">block</span> Đã hết chỗ
                           </div>`
                        : `<div class="font-caption text-caption text-success flex items-center justify-start sm:justify-end mt-1">
                                <span class="material-symbols-outlined text-[14px] mr-1">event_seat</span> Còn ${trip.available_seats} chỗ trống
                           </div>`
                    }
                </div>
                ${isSoldOut
                    ? `<button class="bg-surface-variant text-text-muted font-label-sm text-label-sm h-11 px-6 rounded-lg cursor-not-allowed" disabled>Hết vé</button>`
                    : `<button onclick="goToDetail(${trip.id})" class="bg-primary-container hover:bg-primary text-on-primary font-label-sm text-label-sm h-11 px-6 rounded-lg transition-colors active:scale-95 shadow-sm">Chọn chuyến</button>`
                }
            </div>
        </article>
        `;
    }).join('');
}

function renderEmptyState(isError = false) {
    const container = document.getElementById('trips-container');
    const emptyState = document.getElementById('empty-state');
    const totalCount = document.getElementById('total-trips-count');

    totalCount.textContent = '0';
    container.innerHTML = '';
    container.classList.add('hidden');
    emptyState.classList.remove('hidden');
}

function goToDetail(tripId) {
    window.location.href = `trip-detail.html?trip_id=${tripId}`;
}
