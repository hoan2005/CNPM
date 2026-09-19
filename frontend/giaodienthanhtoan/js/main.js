/** Điều hướng dùng chung cho các màn hình thanh toán và quản lý vé. */
(function () {
    const pageHeader = document.querySelector('body > header');
    if (pageHeader) pageHeader.style.zIndex = '50';

    const modulePages = {
        've-cua-toi': 'chi-tiet-ve.html',
        'tra-cuu-ve': 'tra-cuu-ve.html'
    };

    document.querySelectorAll('[data-path]').forEach(link => {
        const path = link.dataset.path;

        if (modulePages[path]) {
            link.href = modulePages[path];
        } else if (path === 'tim-chuyen' || path === 'trang-chu') {
            link.href = '../../giaodiennguoidung/timkiemchuyenxe/index.html';
        }
    });

    const currentPage = window.location.pathname.split('/').pop();

    if (currentPage === 'tra-cuu-ve.html') {
        wireLookupActions();
    } else if (currentPage === 'nhan-ve.html') {
        const detailLink = document.querySelector('[data-path="ve-cua-toi"]');
        if (detailLink) detailLink.href = 'chi-tiet-ve.html';
    }

    function wireLookupActions() {
        document.querySelectorAll('header .font-headline-sm.text-primary, footer .font-headline-sm.text-primary')
            .forEach(brandName => {
                brandName.textContent = 'VexeExpress';
            });

        const buttons = Array.from(document.querySelectorAll('button'));
        const detailButton = buttons.find(button => button.textContent.includes('Xem chi tiết'));
        const cancelButton = buttons.find(button => button.textContent.includes('Yêu cầu hủy vé'));

        if (detailButton) {
            detailButton.addEventListener('click', () => {
                window.location.href = 'chi-tiet-ve.html';
            });
        }

        if (cancelButton) {
            cancelButton.addEventListener('click', () => {
                window.location.href = 'huy-ve.html';
            });
        }
    }
})();
