const API_URL = "http://localhost:5000/api";
let treeData = {};

// بررسی اتصال به سرور
async function checkConnection() {
  try {
    const response = await fetch(`${API_URL}/people`);
    if (response.ok) {
      document.getElementById("statusBar").className = "status connected";
      document.getElementById("statusBar").textContent =
        "✅ متصل به سرور پایتون";
      return true;
    }
  } catch (error) {
    document.getElementById("statusBar").className = "status disconnected";
    document.getElementById("statusBar").textContent =
      "❌ سرور پایتون در دسترس نیست - لطفاً app.py را اجرا کنید";
    return false;
  }
}

// بارگذاری داده‌ها از سرور
async function loadData() {
  try {
    const response = await fetch(`${API_URL}/people`);
    if (!response.ok) throw new Error("Failed to load data");

    treeData = await response.json();
    updateSelects();
    renderTree();
  } catch (error) {
    console.error("Error loading data:", error);
    showResult("خطا در بارگذاری داده‌ها", true);
  }
}

async function addPerson() {
  const name = document.getElementById("newName").value.trim();
  const gender = document.getElementById("newGender").value;

  if (!name || !gender) {
    showResult("لطفاً نام و جنسیت را وارد کنید", true);
    return;
  }

  try {
    const response = await fetch(`${API_URL}/person`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, gender }),
    });

    const result = await response.json();

    if (result.success) {
      document.getElementById("newName").value = "";
      document.getElementById("newGender").value = "";
      await loadData();
      showResult(`${name} با موفقیت اضافه شد`);
    } else {
      showResult(result.error, true);
    }
  } catch (error) {
    showResult("خطا در ارتباط با سرور", true);
  }
}

async function setFather() {
  const child = document.getElementById("childForFather").value;
  const father = document.getElementById("fatherSelect").value;

  if (!child || !father) {
    showResult("لطفاً هر دو فرد را انتخاب کنید", true);
    return;
  }

  try {
    const response = await fetch(`${API_URL}/father`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ child, father }),
    });

    const result = await response.json();

    if (result.success) {
      await loadData();
      showResult(`${father} به عنوان پدر ${child} تنظیم شد`);
    } else {
      showResult(result.error, true);
    }
  } catch (error) {
    showResult("خطا در ارتباط با سرور", true);
  }
}

async function setMother() {
  const child = document.getElementById("childForMother").value;
  const mother = document.getElementById("motherSelect").value;

  if (!child || !mother) {
    showResult("لطفاً هر دو فرد را انتخاب کنید", true);
    return;
  }

  try {
    const response = await fetch(`${API_URL}/mother`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ child, mother }),
    });

    const result = await response.json();

    if (result.success) {
      await loadData();
      showResult(`${mother} به عنوان مادر ${child} تنظیم شد`);
    } else {
      showResult(result.error, true);
    }
  } catch (error) {
    showResult("خطا در ارتباط با سرور", true);
  }
}

// async function findPath() {
//   const start = document.getElementById("pathStart").value;
//   const end = document.getElementById("pathEnd").value;

//   if (!start || !end) {
//     showResult("لطفاً هر دو فرد را انتخاب کنید", true);
//     return;
//   }

//   try {
//     const response = await fetch(`${API_URL}/path`, {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ start, end }),
//     });

//     const result = await response.json();

//     if (result.success && result.path) {
//       const pathStr = result.path
//         .map((p) => `<span class="path-step">${p}</span>`)
//         .join(" ← ");
//       showResult(`<h4>مسیر از ${start} به ${end}:</h4>${pathStr}`);
//     } else {
//       showResult(result.error || "مسیری پیدا نشد", true);
//     }
//   } catch (error) {
//     showResult("خطا در ارتباط با سرور", true);
//   }
// }

async function findPath() {
  const start = document.getElementById("pathStart").value;
  const end = document.getElementById("pathEnd").value;

  if (!start || !end) {
    showResult("لطفاً هر دو فرد را انتخاب کنید", true);
    return;
  }

  try {
    const response = await fetch(`${API_URL}/path`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ start, end }),
    });

    const result = await response.json();

    if (result.success && result.path) {
      // نمایش نسبت فارسی
      showResult(`
        <h4>رابطه بین ${start} و ${end}:</h4>
        <div class="path-step" style="font-size: 18px; padding: 15px;">
          ${result.path}
        </div>
      `);
    } else {
      showResult(result.error || "مسیری پیدا نشد", true);
    }
  } catch (error) {
    showResult("خطا در ارتباط با سرور", true);
  }
}

function updateSelects() {
  const names = Object.keys(treeData);
  const selects = [
    "childForFather",
    "childForMother",
    "fatherSelect",
    "motherSelect",
    "pathStart",
    "pathEnd",
  ];

  selects.forEach((id) => {
    const select = document.getElementById(id);
    select.innerHTML = '<option value="">انتخاب کنید</option>';
    names.forEach((name) => {
      const option = document.createElement("option");
      option.value = name;
      option.textContent = name;
      select.appendChild(option);
    });
  });
}

function showResult(message, isError = false) {
  const box = document.getElementById("resultBox");
  box.innerHTML = message;
  box.className = "result-box show" + (isError ? " error" : "");
}

// function renderTree() {
//     const treeView = document.getElementById('treeView');
//     treeView.innerHTML = '';
    
//     const roots = Object.values(treeData).filter(p => !p.father && !p.mother);
    
//     if (roots.length === 0) {
//         treeView.innerHTML = '<p style="text-align:center; color:#666;">هنوز فردی اضافه نشده است</p>';
//         return;
//     }

//     const treeDiv = document.createElement('div');
//     treeDiv.style.display = 'flex';
//     treeDiv.style.flexDirection = 'column';
//     treeDiv.style.alignItems = 'center';
//     treeDiv.style.gap = '40px';
    
//     // نمایش هر نسل در یک سطر
//     const levels = getGenerationLevels();
    
//     Object.keys(levels).sort((a, b) => a - b).forEach(level => {
//         const levelDiv = document.createElement('div');
//         levelDiv.style.display = 'flex';
//         levelDiv.style.justifyContent = 'center';
//         levelDiv.style.gap = '30px';
//         levelDiv.style.position = 'relative';
        
//         levels[level].forEach(personName => {
//             const person = treeData[personName];
//             const card = createPersonCard(person);
//             levelDiv.appendChild(card);
//         });
        
//         treeDiv.appendChild(levelDiv);
//     });
    
//     treeView.appendChild(treeDiv);
// }

// function getGenerationLevels() {
//     const levels = {};
//     const visited = new Set();
    
//     function assignLevel(personName, level) {
//         if (visited.has(personName)) return;
//         visited.add(personName);
        
//         if (!levels[level]) levels[level] = [];
//         levels[level].push(personName);
        
//         const person = treeData[personName];
//         if (person.children) {
//             person.children.forEach(childName => {
//                 assignLevel(childName, level + 1);
//             });
//         }
//     }
    
//     // شروع از ریشه‌ها
//     Object.values(treeData).forEach(p => {
//         if (!p.father && !p.mother) {
//             assignLevel(p.name, 0);
//         }
//     });
    
//     return levels;
// }

// function createPersonCard(person) {
//     const card = document.createElement('div');
//     card.className = `person-card ${person.gender}`;
//     card.innerHTML = `
//         <div class="person-name">${person.name}</div>
//         <div class="person-gender">${person.gender === 'male' ? '👨 مرد' : '👩 زن'}</div>
//     `;
//     return card;
// }

// test
function renderTree() {
    const treeView = document.getElementById('treeView');
    treeView.innerHTML = '';

    const roots = Object.values(treeData).filter(
        p => !p.father && !p.mother
    );

    roots.forEach(root => {
        const node = renderPersonNode(root.name);
        treeView.appendChild(node);
    });
}
function renderPersonNode(personName) {
    const person = treeData[personName];

    const container = document.createElement('div');
    container.className = 'tree-node';

    // والدین
    if (person.father || person.mother) {
        const parentsDiv = document.createElement('div');
        parentsDiv.className = 'parents';

        if (person.father) {
            parentsDiv.appendChild(createPersonCard(treeData[person.father]));
        }
        if (person.mother) {
            parentsDiv.appendChild(createPersonCard(treeData[person.mother]));
        }

        container.appendChild(parentsDiv);
        container.appendChild(createLineDown());
    }

    // خود شخص
    container.appendChild(createPersonCard(person));

    // فرزندان
    if (person.children && person.children.length > 0) {
        container.appendChild(createLineDown());

        const childrenDiv = document.createElement('div');
        childrenDiv.className = 'children';

        person.children.forEach(childName => {
            childrenDiv.appendChild(renderPersonNode(childName));
        });

        container.appendChild(childrenDiv);
    }

    return container;
}
function createPersonCard(person) {
    const card = document.createElement('div');
    card.className = `person-card ${person.gender}`;
    card.innerHTML = `
        <div>${person.name}</div>
        <div style="font-size:12px; opacity:0.7">
            ${person.gender === 'male' ? '👨 مرد' : '👩 زن'}
        </div>
    `;
    return card;
}

function createLineDown() {
    const line = document.createElement('div');
    line.className = 'line-down';
    return line;
}


// شروع برنامه
(async function init() {
  const connected = await checkConnection();
  if (connected) {
    await loadData();
  }
})();
