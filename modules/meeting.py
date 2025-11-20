<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>專案會議紀錄 - Firestore 持久化</title>
    <!-- 載入 Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* 使用 Inter 字體以獲得更好的顯示效果 */
        :root {
            font-family: 'Inter', sans-serif;
        }
    </style>
    <!-- 載入 Firebase 函式庫 -->
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
        import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
        import { getFirestore, collection, doc, setDoc, addDoc, deleteDoc, onSnapshot, query, orderBy, serverTimestamp, getDocs, updateDoc } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";
        import { setLogLevel } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";

        // 全域變數
        const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
        const firebaseConfig = JSON.parse(typeof __firebase_config !== 'undefined' ? __firebase_config : '{}');
        const initialAuthToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : null;

        let db;
        let auth;
        let userId = null;
        let currentProjectNo = 'PJ202501'; // 預設專案編號

        // --- Firebase 初始化與認證 ---
        const initFirebase = async () => {
            if (Object.keys(firebaseConfig).length === 0) {
                console.error("Firebase 配置未提供，無法初始化。");
                document.getElementById('app').innerHTML = '<div class="text-red-600 p-4">錯誤：Firebase 配置未載入。</div>';
                return;
            }

            try {
                setLogLevel('debug'); // 開啟 Firestore 偵錯日誌
                const app = initializeApp(firebaseConfig);
                db = getFirestore(app);
                auth = getAuth(app);

                // 認證: 使用提供的 token 或匿名登入
                if (initialAuthToken) {
                    await signInWithCustomToken(auth, initialAuthToken);
                } else {
                    await signInAnonymously(auth);
                }
                
                onAuthStateChanged(auth, (user) => {
                    if (user) {
                        userId = user.uid;
                        document.getElementById('current-user-id').textContent = userId;
                        console.log("Firebase 認證成功，User ID:", userId);
                        // 認證成功後啟動應用邏輯
                        setupAppListeners();
                    } else {
                        console.log("Firebase 認證失敗或登出。");
                    }
                });

            } catch (error) {
                console.error("Firebase 初始化或認證錯誤:", error);
                document.getElementById('app').innerHTML = `<div class="text-red-600 p-4">錯誤：認證失敗。${error.message}</div>`;
            }
        };
        
        // --- Firestore 互動函式 ---
        const getCollectionRef = (projectNo) => {
            // 使用公開路徑以利協作，路徑為: /artifacts/{appId}/public/data/meeting_records_{projectNo}
            return collection(db, 'artifacts', appId, 'public', 'data', `meeting_records_${projectNo}`);
        };

        const displayMessage = (message, type = 'success') => {
            const container = document.getElementById('message-container');
            container.innerHTML = `<div class="p-3 mb-4 rounded-lg text-sm font-medium ${type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">${message}</div>`;
            setTimeout(() => container.innerHTML = '', 3000);
        };
        
        // --- CRUD 操作 ---

        // 監聽並顯示資料
        const setupAppListeners = () => {
            const projectInput = document.getElementById('project-input');
            projectInput.value = currentProjectNo;
            projectInput.addEventListener('change', (e) => {
                currentProjectNo = e.target.value;
                document.getElementById('project-header').textContent = `${currentProjectNo} 專案會議紀錄`;
                listenForRecords(currentProjectNo);
            });

            // 首次載入或專案變更時開始監聽
            listenForRecords(currentProjectNo);
            
            // 設定新增表單提交事件
            document.getElementById('add-form').addEventListener('submit', handleAddRecord);
        };

        let currentUnsubscribe = null;

        const listenForRecords = (projectNo) => {
            if (currentUnsubscribe) {
                currentUnsubscribe(); // 取消先前的監聽
            }

            const q = query(getCollectionRef(projectNo), orderBy('日期', 'desc'));
            const tableBody = document.getElementById('records-table-body');
            const downloadButton = document.getElementById('download-csv-btn');
            
            tableBody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-gray-500">載入中...</td></tr>';
            downloadButton.onclick = null; // 清除舊的下載事件

            currentUnsubscribe = onSnapshot(q, (snapshot) => {
                const records = [];
                snapshot.forEach((doc) => {
                    records.push({ id: doc.id, ...doc.data() });
                });
                renderRecordsTable(records);
            }, (error) => {
                console.error("監聽 Firestore 錯誤:", error);
                displayMessage("載入資料失敗。", 'error');
                tableBody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-red-500">資料載入錯誤</td></tr>';
            });
        };

        const handleAddRecord = async (e) => {
            e.preventDefault();
            const form = e.target;
            const dateInput = form.querySelector('#date-input').value;
            
            // 檢查必填欄位 (日期和主題)
            if (!dateInput || !form.querySelector('#subject-input').value) {
                displayMessage("日期和主題為必填欄位！", 'error');
                return;
            }

            const newRecord = {
                日期: new Date(dateInput), // 儲存為 Timestamp
                地點: form.querySelector('#location-input').value || '未填寫',
                主題: form.querySelector('#subject-input').value,
                主持人: form.querySelector('#host-input').value || '未填寫',
                出席人員: form.querySelector('#attendees-input').value || '未填寫',
                會議記錄: form.querySelector('#note-input').value,
                createdAt: serverTimestamp() // 加入時間戳
            };

            try {
                await addDoc(getCollectionRef(currentProjectNo), newRecord);
                displayMessage("🎉 新增成功！");
                form.reset(); // 清空表單
                form.querySelector('#date-input').valueAsDate = new Date(); // 重設日期為今天
            } catch (error) {
                console.error("新增記錄錯誤:", error);
                displayMessage("新增記錄失敗：" + error.message, 'error');
            }
        };

        const handleDeleteRecord = async (id) => {
            if (!confirm("確定要刪除這筆會議紀錄嗎？")) return;
            try {
                const docRef = doc(getCollectionRef(currentProjectNo), id);
                await deleteDoc(docRef);
                displayMessage("🗑️ 刪除成功！");
            } catch (error) {
                console.error("刪除記錄錯誤:", error);
                displayMessage("刪除記錄失敗：" + error.message, 'error');
            }
        };

        const handleEditRecord = (record) => {
             // 填充 Modal/Form 資料
            document.getElementById('edit-id').value = record.id;
            document.getElementById('edit-date').value = record.日期.toDate().toISOString().split('T')[0];
            document.getElementById('edit-location').value = record.地點;
            document.getElementById('edit-subject').value = record.主題;
            document.getElementById('edit-host').value = record.主持人;
            document.getElementById('edit-attendees').value = record.出席人員;
            document.getElementById('edit-note').value = record.會議記錄;
            
            // 顯示 Modal
            document.getElementById('edit-modal').classList.remove('hidden');
        };

        const handleUpdateRecord = async (e) => {
            e.preventDefault();
            const form = e.target;
            const id = form.querySelector('#edit-id').value;
            
            const updatedData = {
                日期: new Date(form.querySelector('#edit-date').value),
                地點: form.querySelector('#edit-location').value,
                主題: form.querySelector('#edit-subject').value,
                主持人: form.querySelector('#edit-host').value,
                出席人員: form.querySelector('#edit-attendees').value,
                會議記錄: form.querySelector('#edit-note').value,
            };

            try {
                const docRef = doc(db, 'artifacts', appId, 'public', 'data', `meeting_records_${currentProjectNo}`, id);
                await updateDoc(docRef, updatedData);
                displayMessage("✅ 修改成功！");
                document.getElementById('edit-modal').classList.add('hidden');
            } catch (error) {
                console.error("修改記錄錯誤:", error);
                displayMessage("修改記錄失敗：" + error.message, 'error');
            }
        };
        
        // 匯出 CSV 函式
        const exportToCSV = (records) => {
            if (records.length === 0) return;

            const header = ["日期", "地點", "主題", "主持人", "出席人員", "會議記錄"];
            let csv = '\ufeff' + header.join(',') + '\n'; // \ufeff is BOM for UTF-8 in Excel

            records.forEach(record => {
                const dateStr = record.日期 ? record.日期.toDate().toLocaleDateString('zh-TW', { year: 'numeric', month: '2-digit', day: '2-digit' }) : 'N/A';
                // 確保內容中的逗號被引號包圍
                const safeValue = (val) => `"${String(val).replace(/"/g, '""')}"`;
                
                const row = [
                    safeValue(dateStr),
                    safeValue(record.地點),
                    safeValue(record.主題),
                    safeValue(record.主持人),
                    safeValue(record.出席人員),
                    safeValue(record.會議記錄)
                ];
                csv += row.join(',') + '\n';
            });

            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8-sig;' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.setAttribute('href', url);
            a.setAttribute('download', `Meeting_${currentProjectNo}_${new Date().toISOString().split('T')[0]}.csv`);
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        };
        
        // --- 渲染 UI 函式 ---
        const renderRecordsTable = (records) => {
            const tableBody = document.getElementById('records-table-body');
            const downloadButton = document.getElementById('download-csv-btn');
            
            tableBody.innerHTML = '';
            
            if (records.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="7" class="text-center py-8 text-gray-500 text-lg">目前沒有會議記錄。請新增一筆。</td></tr>';
                downloadButton.classList.add('hidden');
                return;
            }

            downloadButton.classList.remove('hidden');
            downloadButton.onclick = () => exportToCSV(records);


            records.forEach((record, index) => {
                // 將 Firebase Timestamp 轉換為 Date 物件並格式化
                const dateStr = record.日期 ? record.日期.toDate().toLocaleDateString('zh-TW', { timeZone: 'Asia/Taipei' }) : 'N/A';
                
                const row = document.createElement('tr');
                row.className = index % 2 === 0 ? 'bg-white hover:bg-gray-50' : 'bg-gray-50 hover:bg-gray-100';
                
                row.innerHTML = `
                    <td class="px-6 py-3 whitespace-nowrap text-sm font-medium text-gray-900">${records.length - 1 - index}</td>
                    <td class="px-6 py-3 whitespace-nowrap text-sm text-gray-500">${dateStr}</td>
                    <td class="px-6 py-3 text-sm font-medium text-gray-900 truncate max-w-xs">${record.主題}</td>
                    <td class="px-6 py-3 whitespace-nowrap text-sm text-gray-500">${record.主持人}</td>
                    <td class="px-6 py-3 text-sm text-gray-500 truncate max-w-xs">${record.會議記錄}</td>
                    <td class="px-6 py-3 whitespace-nowrap text-sm text-gray-500">${record.出席人員}</td>
                    <td class="px-6 py-3 whitespace-nowrap text-sm font-medium">
                        <button id="edit-${record.id}" class="text-indigo-600 hover:text-indigo-900 mr-3 p-1.5 rounded-full hover:bg-indigo-100 transition duration-150">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-7-9l4 4m-4-4l-9 9m10 0l-4-4m-9 9l-4-4"></path></svg>
                        </button>
                        <button id="delete-${record.id}" class="text-red-600 hover:text-red-900 p-1.5 rounded-full hover:bg-red-100 transition duration-150">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                        </button>
                    </td>
                `;
                tableBody.appendChild(row);

                // 綁定事件
                document.getElementById(`edit-${record.id}`).addEventListener('click', () => handleEditRecord(record));
                document.getElementById(`delete-${record.id}`).addEventListener('click', () => handleDeleteRecord(record.id));
            });
        };

        // --- 啟動應用 ---
        document.addEventListener('DOMContentLoaded', () => {
             // 隱藏 Modal
            document.getElementById('edit-modal').classList.add('hidden');
            document.getElementById('edit-form-modal').addEventListener('submit', handleUpdateRecord);
            document.getElementById('close-modal-btn').addEventListener('click', () => {
                 document.getElementById('edit-modal').classList.add('hidden');
            });
            
            // 預設日期為今天
            document.getElementById('date-input').valueAsDate = new Date();
            
            initFirebase();
        });

        // 將函式暴露給外部，方便在 HTML 中呼叫 (雖然此處我們主要在 JS 內部處理)
        window.handleEditRecord = handleEditRecord;
        window.handleDeleteRecord = handleDeleteRecord;
        window.exportToCSV = exportToCSV;

    </script>
</head>
<body class="bg-gray-100 min-h-screen">
    <div id="app" class="container mx-auto p-4 md:p-8 max-w-6xl">
        
        <!-- 標題與專案選擇 -->
        <div class="bg-white shadow-lg rounded-xl p-6 mb-8">
            <h1 class="text-3xl font-bold text-gray-800 mb-4" id="project-header">PJ202501 專案會議紀錄</h1>
            <div class="flex items-center space-x-4 text-sm text-gray-600">
                <label for="project-input" class="font-medium">切換或輸入專案編號:</label>
                <input type="text" id="project-input" value="PJ202501" class="border border-gray-300 rounded-lg p-2 focus:ring-indigo-500 focus:border-indigo-500 w-40 transition duration-150">
            </div>
            <p class="mt-2 text-xs text-gray-400">當前使用者 ID: <span id="current-user-id" class="font-mono text-gray-500">認證中...</span></p>
        </div>

        <!-- 訊息顯示區 -->
        <div id="message-container"></div>
        
        <!-- 新增會議記錄表單 -->
        <div class="bg-white shadow-lg rounded-xl p-6 mb-8">
            <h2 class="text-xl font-semibold text-indigo-600 mb-4">➕ 新增會議記錄</h2>
            <form id="add-form" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label for="date-input" class="block text-sm font-medium text-gray-700">日期 <span class="text-red-500">*</span></label>
                        <input type="date" id="date-input" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border">
                    </div>
                    <div>
                        <label for="subject-input" class="block text-sm font-medium text-gray-700">主題 <span class="text-red-500">*</span></label>
                        <input type="text" id="subject-input" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border" placeholder="輸入會議主題">
                    </div>
                    <div>
                        <label for="location-input" class="block text-sm font-medium text-gray-700">地點</label>
                        <input type="text" id="location-input" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border" placeholder="會議地點">
                    </div>
                    <div>
                        <label for="host-input" class="block text-sm font-medium text-gray-700">主持人</label>
                        <input type="text" id="host-input" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border" placeholder="主持人姓名">
                    </div>
                </div>
                <div>
                    <label for="attendees-input" class="block text-sm font-medium text-gray-700">出席人員 (請用逗號或空格分隔)</label>
                    <textarea id="attendees-input" rows="2" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border"></textarea>
                </div>
                 <div>
                    <label for="note-input" class="block text-sm font-medium text-gray-700">會議記錄/摘要</label>
                    <textarea id="note-input" rows="4" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border" placeholder="輸入會議的主要內容、決議事項和行動項目"></textarea>
                </div>
                <button type="submit" class="w-full inline-flex justify-center py-3 px-4 border border-transparent shadow-sm text-base font-medium rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150">
                    💾 儲存並新增記錄
                </button>
            </form>
        </div>

        <!-- 所有會議紀錄表格 -->
        <div class="bg-white shadow-lg rounded-xl p-6 mb-8">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">📋 所有會議記錄</h2>
            
            <div class="flex justify-end mb-4">
                 <button id="download-csv-btn" class="hidden bg-green-500 hover:bg-green-600 text-white font-medium py-2 px-4 rounded-lg shadow transition duration-150">
                    ⬇️ 下載 CSV (中文支援)
                </button>
            </div>
            
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200 rounded-lg">
                    <thead class="bg-indigo-50">
                        <tr>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-16">#</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">日期</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">主題</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">主持人</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider max-w-xs">記錄摘要</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider max-w-xs">出席人員</th>
                            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-32">操作</th>
                        </tr>
                    </thead>
                    <tbody id="records-table-body" class="bg-white divide-y divide-gray-200">
                        <!-- 資料將由 JavaScript 動態載入 -->
                    </tbody>
                </table>
            </div>
        </div>
        
    </div>

    <!-- 編輯 Modal (彈出視窗) -->
    <div id="edit-modal" class="fixed inset-0 bg-gray-600 bg-opacity-75 overflow-y-auto h-full w-full z-50 transition duration-300 hidden">
        <div class="relative top-10 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-xl rounded-xl bg-white">
            <div class="flex justify-between items-center pb-3">
                <h3 class="text-xl font-semibold text-gray-900">✏️ 編輯會議紀錄</h3>
                <button id="close-modal-btn" type="button" class="text-gray-400 hover:text-gray-900 transition duration-150">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
            </div>
            <div class="mt-2">
                <form id="edit-form-modal" class="space-y-4">
                    <input type="hidden" id="edit-id">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label for="edit-date" class="block text-sm font-medium text-gray-700">日期</label>
                            <input type="date" id="edit-date" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border">
                        </div>
                        <div>
                            <label for="edit-subject" class="block text-sm font-medium text-gray-700">主題</label>
                            <input type="text" id="edit-subject" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border">
                        </div>
                    </div>
                    <div>
                        <label for="edit-location" class="block text-sm font-medium text-gray-700">地點</label>
                        <input type="text" id="edit-location" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border">
                    </div>
                    <div>
                        <label for="edit-host" class="block text-sm font-medium text-gray-700">主持人</label>
                        <input type="text" id="edit-host" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border">
                    </div>
                    <div>
                        <label for="edit-attendees" class="block text-sm font-medium text-gray-700">出席人員</label>
                        <textarea id="edit-attendees" rows="2" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border"></textarea>
                    </div>
                    <div>
                        <label for="edit-note" class="block text-sm font-medium text-gray-700">會議記錄/摘要</label>
                        <textarea id="edit-note" rows="4" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border"></textarea>
                    </div>
                    <div class="mt-4 flex justify-end space-x-3">
                        <button type="button" id="cancel-edit-btn" onclick="document.getElementById('edit-modal').classList.add('hidden')" class="py-2 px-4 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition duration-150">
                            取消
                        </button>
                        <button type="submit" class="py-2 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 transition duration-150">
                            💾 確認修改
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

</body>
</html>
