const apiUrl = "http://127.0.0.1:8000";

function readFileContent(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => resolve(event.target.result);
        reader.onerror = (error) => reject(error);
        reader.readAsText(file);
    });
}

async function createScript(event) {
    event.preventDefault();
    const form = document.getElementById('new-script-form');
    const name = form.elements.name.value;
    const mainCodeFile = form.elements.mainCode.files[0];
    const triggerCodeFile = form.elements.triggerCode.files[0];

    if (!name || !mainCodeFile || !triggerCodeFile) {
        alert('Please fill out all fields and select both code files.');
        return;
    }

    try {
        const mainCode = await readFileContent(mainCodeFile);
        const triggerCode = await readFileContent(triggerCodeFile);

        const response = await fetch(`${apiUrl}/script/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "name": name,
                "triggerCode": triggerCode,
                "mainCode": mainCode,
            }),
        });

        if (response.ok) {
            form.reset();
            getScripts();
        } else {
            const error = await response.json();
            console.error('Failed to create script:', error);
            alert(`Error: ${error.detail || 'Could not create script.'}`);
        }
    } catch (error) {
        console.error('Error creating script:', error);
        alert('An error occurred while creating the script.');
    }
}


async function getScripts() {
    try {
        const response = await fetch(`${apiUrl}/scripts/`,
            {
                method: 'GET',
                redirect: "follow",
                headers: {
                    'accept': 'application/json',
                },
        }
        );
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const scripts = await response.json();
        const scriptsContainer = document.getElementById('current-scripts');
        scriptsContainer.innerHTML = '';

        if (scripts.length === 0) {
            scriptsContainer.innerHTML = '<p>No scripts have been created yet.</p>';
            return;
        }

        
        
        const ul = document.createElement('ul');
        scripts.forEach(script => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span>${script.name} (ID: ${script.id})</span>
                <button onclick="deleteScript('${script.id}')">Delete</button>
            `;
            ul.appendChild(li);
        });
        scriptsContainer.appendChild(ul);
    } catch (error) {
        
        console.error('Error fetching scripts:', error);
        document.getElementById('current-scripts').innerHTML = '<p>Could not load scripts.</p>';
    }
}


async function deleteScript(id) {
    if (!confirm('Are you sure you want to delete this script?')) {
        return;
    }

    try {
        const response = await fetch(`${apiUrl}/script/${id}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            getScripts();
        } else {
            const error = await response.json();
            console.error('Failed to delete script:', error);
            alert(`Error: ${error.detail || 'Could not delete script.'}`);
        }
    } catch (error) {
        console.error('Error deleting script:', error);
        alert('An error occurred while deleting the script.');
    }
}


document.addEventListener('DOMContentLoaded', () => {
    const newScriptForm = document.getElementById('new-script-form');
    newScriptForm.addEventListener('submit', createScript);
    
    
    const reloadButton = document.getElementById('reload-button');
    reloadButton.addEventListener('click', getScripts);

    getScripts();
});