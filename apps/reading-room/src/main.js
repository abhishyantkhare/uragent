import { createClient } from '@supabase/supabase-js';
import './style.css';

const collection = document.querySelector('#collection');
const status = document.querySelector('#connection');
const search = document.querySelector('#search');
const tabs = [...document.querySelectorAll('[data-category]')];
let books = [];
let category = 'all';

function render() {
  const query = search.value.trim().toLowerCase();
  const visible = books.filter((book) =>
    (category === 'all' || book.category === category)
    && `${book.title} ${book.author}`.toLowerCase().includes(query));
  collection.replaceChildren();
  for (const book of visible) {
    const article = document.createElement('article');
    article.className = 'book';
    const cover = document.createElement('div');
    cover.className = `cover ${book.category}`;
    const initial = document.createElement('span');
    initial.textContent = book.title.slice(0, 1);
    cover.append(initial);
    const text = document.createElement('div');
    const kind = document.createElement('p');
    kind.className = 'eyebrow';
    kind.textContent = book.category === 'essay' ? 'ESSAY' : 'BOOK';
    const title = document.createElement('h2');
    title.textContent = book.title;
    const author = document.createElement('p');
    author.className = 'author';
    author.textContent = book.author;
    const note = document.createElement('p');
    note.className = 'note';
    note.textContent = book.note;
    text.append(kind, title, author, note);
    article.append(cover, text);
    collection.append(article);
  }
  status.textContent = visible.length ? `${visible.length} things worth reading` : 'No matching titles.';
}

search.addEventListener('input', render);
for (const tab of tabs) {
  tab.addEventListener('click', () => {
    category = tab.dataset.category;
    for (const button of tabs) button.setAttribute('aria-pressed', String(button === tab));
    render();
  });
}

async function loadCollection() {
  const url = import.meta.env.VITE_SUPABASE_URL;
  const key = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY;
  if (!url || !key) {
    status.textContent = 'Setup required: connect this app to Supabase using VITE_SUPABASE_URL and VITE_SUPABASE_PUBLISHABLE_KEY.';
    return;
  }
  const client = createClient(url, key);
  const { data, error } = await client.from('reading_room_books_retry')
    .select('id,title,author,category,note').order('id');
  if (error) {
    status.textContent = `The collection could not load: ${error.message}`;
    return;
  }
  books = data;
  render();
}

loadCollection().catch(() => {
  status.textContent = 'The collection could not connect. Please try again later.';
});
