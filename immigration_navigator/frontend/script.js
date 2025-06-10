async function postData(url = '', data = {}) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });
  return response.json();
}

document.getElementById('immigration-form').onsubmit = async (e) => {
  e.preventDefault();
  const formData = Object.fromEntries(new FormData(e.target));
  const res = await postData('/api/immigration', formData);
  document.getElementById('immigration-result').innerText = JSON.stringify(res, null, 2);
};

document.getElementById('form-fill').onsubmit = async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  const res = await postData('/api/fill_form', data);
  const link = document.getElementById('pdf-link');
  link.href = 'data:application/pdf;base64,' + res.pdf_base64;
  link.style.display = 'inline';
};

document.getElementById('wellness-form').onsubmit = async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  const res = await postData('/api/wellness', data);
  document.getElementById('wellness-result').innerText = JSON.stringify(res, null, 2);
};

document.getElementById('translate-form').onsubmit = async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  const res = await postData('/api/translate', data);
  document.getElementById('translate-result').innerText = res.translation;
};

document.getElementById('load-timeline').onclick = async () => {
  const res = await fetch('/api/timeline');
  const data = await res.json();
  document.getElementById('timeline').innerText = JSON.stringify(data.events, null, 2);
};
