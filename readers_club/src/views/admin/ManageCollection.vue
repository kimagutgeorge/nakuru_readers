<template>
    <div class="admin-panel col-flex">
        <div class="col-100">
            <p><span  class="title-label">Manage</span> <span class="title-label-small"><i class="fa-solid fa-angle-right"></i> Collections</span></p>
        </div>
        <div class="col-100 admin-panel-body col-flex">
            <div class="col-30">
                <p class="title-label">Add Collection</p>
                <div class="form-group">
                    <label class="title-label-small">Collection Name</label>
                    <input type="text" v-model="collection_name" class="universal-input form-input" placeholder="Favourites">
                </div>
                <div class="form-group">
                    <label class="title-label-small">Book</label>
                    <select class="universal-input form-input" v-model="selected_book" @change="selectBook" id="selected_book">
                        <option value="1">Book one</option>
                        <option value="2">Book two</option>
                        <option value="3">Book three</option>
                    </select>
                </div>
                <div class="form-group col-flex">
                    <div class="book-list col-flex" v-for="(single_book, index) in selectedbooks" :key="index">
                        <p><span hidden>{{ single_book.id }}</span><span class="text-dark-gray">{{ single_book.name }}</span> <span><i class="fa-solid fa-close" @click="removeBook(single_book.id)"></i></span></p>
                    </div>
                </div>
                <div class="form-group">
                    <button class="btn btn-success">SUBMIT</button>
                </div>
            </div>
            <div class="col-70">
                <!-- insert data here -->
            </div>
        </div>
    </div>
</template>
<script>
export default {
  name: 'ManageBook',
  data () {
    return {
        selected_book: '',
        collection_name: '',
        selectedbooks: [],
    } 
  },
  methods: {
    selectBook() {
        const currentBook = this.selected_book
        const selectedBook = document.getElementById('selected_book')
        const bookOption = selectedBook.options[selectedBook.selectedIndex].text
        if (!this.selectedbooks.find(book => book.id === currentBook)) {
            this.selectedbooks.push({
                'name': bookOption,
                'id': currentBook
            })
        } 
    },
    removeBook(id) {
        const index = this.selectedbooks.findIndex(book => book.id === id);
        if (index !== -1) {
            this.selectedbooks.splice(index, 1); // Remove the book at the found index
        }
    }
  }
}
</script>