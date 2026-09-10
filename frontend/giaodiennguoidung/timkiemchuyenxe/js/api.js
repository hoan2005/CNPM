/**
 * TransLink API Service
 * Xử lý toàn bộ giao tiếp giữa Frontend và Backend RESTful API
 */
const BASE_URL = 'http://127.0.0.1:8000';

const TransLinkAPI = {
    /**
     * Tìm kiếm chuyến xe và áp dụng bộ lọc
     */
    async searchTrips(params = {}) {
        const queryParams = new URLSearchParams();

        if (params.departure) queryParams.append('departure', params.departure.trim());
        if (params.destination) queryParams.append('destination', params.destination.trim());
        if (params.travelDate) queryParams.append('travel_date', params.travelDate);
        if (params.passengers) queryParams.append('passengers', params.passengers);
        if (params.minPrice) queryParams.append('min_price', params.minPrice);
        if (params.maxPrice) queryParams.append('max_price', params.maxPrice);
        if (params.timeSlot) queryParams.append('time_slot', params.timeSlot);
        if (params.sortBy) queryParams.append('sort_by', params.sortBy);
        if (params.sortOrder) queryParams.append('sort_order', params.sortOrder);

        if (params.busTypes && params.busTypes.length > 0) {
            params.busTypes.forEach(bt => queryParams.append('bus_type', bt));
        }

        if (params.operators && params.operators.length > 0) {
            params.operators.forEach(op => queryParams.append('operator', op));
        }

        const url = `${BASE_URL}/api/trips/search?${queryParams.toString()}`;
        const response = await fetch(url);
        const data = await response.json();

        if (!response.ok) {
            // Trả về đối tượng lỗi để controller frontend xử lý (VD: Ngoại lệ E1: 400 Bad Request)
            const errorMsg = data.detail || 'Đã có lỗi xảy ra khi tìm kiếm chuyến xe.';
            throw new Error(errorMsg);
        }

        return data;
    },

    /**
     * Lấy thông tin chi tiết một chuyến xe
     */
    async getTripDetail(tripId) {
        const response = await fetch(`${BASE_URL}/api/trips/${tripId}`);
        if (!response.ok) {
            throw new Error('Không tìm thấy thông tin chuyến xe.');
        }
        return await response.json();
    },

    /**
     * Lấy sơ đồ ghế và tình trạng ghế theo tầng của chuyến xe
     */
    async getSeatMap(tripId) {
        const response = await fetch(`${BASE_URL}/api/trips/${tripId}/seats`);
        if (!response.ok) {
            throw new Error('Không thể tải sơ đồ ghế.');
        }
        return await response.json();
    }
};

window.TransLinkAPI = TransLinkAPI;
