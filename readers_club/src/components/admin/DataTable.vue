<template>
    <div class="table-container">
      <input
        v-if="enableSearch"
        type="text"
        v-model="searchQuery"
        class="form-input universal-input"
        placeholder="Search..."
      />
      <table class="col-100 my-tbl" cellspacing="0">
        <thead>
          <tr>
            <th
              v-for="col in columns"
              :key="col.key"
              @click="sortTable(col.key)"
              style="cursor: pointer"
            >
              {{ col.label }}
              <span
                v-if="sortKey === col.key"
                class="ms-2"
                :class="sortOrder === 'asc' ? 'bi bi-arrow-up' : 'bi bi-arrow-down'"
              ></span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in paginatedData" :key="index">
            <td v-for="col in columns" :key="col.key">{{ row[col.key] }}</td>
          </tr>
        </tbody>
      </table>
      <nav v-if="enablePagination">
        <ul class="pagination col-50 col-flex">
          <li
            class="page-item"
            :class="{ disabled: currentPage === 1 }"
            @click="changePage(currentPage - 1)"
          >
            <a class="page-link" href="#"><i class="fa-solid fa-angle-left"></i></a>
          </li>
          <li
            v-for="page in totalPages"
            :key="page"
            class="page-item"
            :class="{ active: currentPage === page }"
            @click="changePage(page)"
          >
            <a class="page-link" href="#">{{ page }}</a>
          </li>
          <li
            class="page-item"
            :class="{ disabled: currentPage === totalPages }"
            @click="changePage(currentPage + 1)"
          >
            <a class="page-link" href="#"><i class="fa-solid fa-angle-right"></i></a>
          </li>
        </ul>
      </nav>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      data: {
        type: Array,
        required: true,
      },
      columns: {
        type: Array,
        required: true,
      },
      rowsPerPage: {
        type: Number,
        default: 5,
      },
      enableSearch: {
        type: Boolean,
        default: true,
      },
      enablePagination: {
        type: Boolean,
        default: true,
      },
    },
    data() {
      return {
        searchQuery: "",
        sortKey: "",
        sortOrder: "asc",
        currentPage: 1,
      };
    },
    computed: {
      filteredData() {
        if (!this.searchQuery) return this.data;
        return this.data.filter((row) =>
          Object.values(row).some((value) =>
            value.toString().toLowerCase().includes(this.searchQuery.toLowerCase())
          )
        );
      },
      sortedData() {
        if (!this.sortKey) return this.filteredData;
        return [...this.filteredData].sort((a, b) => {
          const aValue = a[this.sortKey];
          const bValue = b[this.sortKey];
          if (this.sortOrder === "asc") return aValue > bValue ? 1 : -1;
          return aValue < bValue ? 1 : -1;
        });
      },
      paginatedData() {
        if (!this.enablePagination) return this.sortedData;
        const start = (this.currentPage - 1) * this.rowsPerPage;
        const end = start + this.rowsPerPage;
        return this.sortedData.slice(start, end);
      },
      totalPages() {
        return Math.ceil(this.sortedData.length / this.rowsPerPage);
      },
    },
    methods: {
      sortTable(column) {
        if (this.sortKey === column) {
          this.sortOrder = this.sortOrder === "asc" ? "desc" : "asc";
        } else {
          this.sortKey = column;
          this.sortOrder = "asc";
        }
      },
      changePage(page) {
        if (page > 0 && page <= this.totalPages) {
          this.currentPage = page;
        }
      },
    },
  };
  </script>
  