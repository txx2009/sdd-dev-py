<template>
  <div class="user-manage">
    <a-card class="user-card">
      <template #title>
        <div class="header">
          <h2>用户管理</h2>
          <a-button type="primary" @click="handleCreate" class="add-button">
            新增用户
          </a-button>
        </div>
      </template>

      <a-table
        :dataSource="users"
        :columns="columns"
        :loading="loading"
        :pagination="paginationConfig"
        rowKey="id"
        class="user-table"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <a-tag :color="record.status === 1 ? 'success' : 'error'" class="status-tag">
              {{ record.status === 1 ? '正常' : '禁用' }}
            </a-tag>
          </template>
          <template v-else-if="column.key === 'createdAt'">
            {{ formatDate(record.createdAt) }}
          </template>
          <template v-else-if="column.key === 'action'">
            <a-space>
              <a-button size="small" @click="handleEdit(record)" class="action-button">
                编辑
              </a-button>
              <a-popconfirm
                title="确认删除该用户?"
                ok-text="确认"
                cancel-text="取消"
                @confirm="handleDelete(record)"
              >
                <a-button size="small" type="primary" danger class="action-button">
                  删除
                </a-button>
              </a-popconfirm>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>

    <!-- 新增/编辑弹窗 -->
    <a-modal
      v-model:open="dialogVisible"
      :title="dialogTitle"
      @ok="handleSubmit"
      :confirmLoading="submitLoading"
      class="user-modal"
    >
      <a-form
        ref="dialogFormRef"
        :model="dialogForm"
        :rules="dialogRules"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 16 }"
      >
        <a-form-item label="用户名" name="username">
          <a-input v-model:value="dialogForm.username" :disabled="!!dialogForm.id" />
        </a-form-item>
        <a-form-item :label="dialogForm.id ? '密码' : '密码'" :name="dialogForm.id ? undefined : 'password'">
          <a-input-password
            v-model:value="dialogForm.password"
            :placeholder="dialogForm.id ? '留空则不修改' : '请输入密码'"
          />
        </a-form-item>
        <a-form-item label="昵称" name="nickname">
          <a-input v-model:value="dialogForm.nickname" />
        </a-form-item>
        <a-form-item label="邮箱" name="email">
          <a-input v-model:value="dialogForm.email" />
        </a-form-item>
        <a-form-item label="手机号" name="phone">
          <a-input v-model:value="dialogForm.phone" />
        </a-form-item>
        <a-form-item label="状态" name="status">
          <a-radio-group v-model:value="dialogForm.status">
            <a-radio :value="1">正常</a-radio>
            <a-radio :value="0">禁用</a-radio>
          </a-radio-group>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { listUsers, createUser, updateUser, deleteUser } from '@/api/user';

const users = ref([]);
const loading = ref(false);
const dialogVisible = ref(false);
const submitLoading = ref(false);
const dialogFormRef = ref(null);

const paginationConfig = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total) => `共 ${total} 条`,
  pageSizeOptions: ['10', '20', '50'],
  onChange: (page, pageSize) => {
    paginationConfig.current = page;
    paginationConfig.pageSize = pageSize;
    fetchUsers();
  },
  onShowSizeChange: (current, size) => {
    paginationConfig.current = 1;
    paginationConfig.pageSize = size;
    fetchUsers();
  },
});

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
  { title: '用户名', dataIndex: 'username', key: 'username' },
  { title: '昵称', dataIndex: 'nickname', key: 'nickname' },
  { title: '邮箱', dataIndex: 'email', key: 'email' },
  { title: '手机号', dataIndex: 'phone', key: 'phone' },
  { title: '状态', dataIndex: 'status', key: 'status', width: 100 },
  { title: '创建时间', dataIndex: 'createdAt', key: 'createdAt', width: 180 },
  { title: '操作', key: 'action', width: 200 },
];

const dialogForm = reactive({
  id: null,
  username: '',
  password: '',
  nickname: '',
  email: '',
  phone: '',
  status: 1,
});

const dialogRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
};

const dialogTitle = computed(() => dialogForm.id ? '编辑用户' : '新增用户');

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleString('zh-CN');
};

const fetchUsers = async () => {
  try {
    loading.value = true;
    const response = await listUsers({
      $page: paginationConfig.current,
      $size: paginationConfig.pageSize,
    });
    users.value = response.data || [];
    paginationConfig.total = response.total || 0;
  } catch (error) {
    message.error('获取用户列表失败');
  } finally {
    loading.value = false;
  }
};

const handleCreate = () => {
  Object.assign(dialogForm, { id: null, username: '', password: '', nickname: '', email: '', phone: '', status: 1 });
  dialogVisible.value = true;
};

const handleEdit = (record) => {
  Object.assign(dialogForm, { ...record, password: '' });
  dialogVisible.value = true;
};

const handleSubmit = async () => {
  try {
    await dialogFormRef.value.validate();
    submitLoading.value = true;
    if (dialogForm.id) {
      await updateUser(dialogForm.id, dialogForm);
      message.success('更新成功');
    } else {
      await createUser(dialogForm);
      message.success('创建成功');
    }
    dialogVisible.value = false;
    fetchUsers();
  } catch (error) {
    if (error.errorFields) {
      return;
    }
    message.error(error.message || '操作失败');
  } finally {
    submitLoading.value = false;
  }
};

const handleDelete = async (record) => {
  try {
    await deleteUser(record.id);
    message.success('删除成功');
    fetchUsers();
  } catch (error) {
    message.error(error.message || '删除失败');
  }
};

onMounted(() => {
  fetchUsers();
});
</script>

<style scoped lang="less">
.user-manage {
  padding: 24px;
}

.user-card {
  background: var(--color-card-bg);
  border: 1px solid var(--color-card-border);
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--transition-normal);

  &:hover {
    box-shadow: var(--shadow-md);
  }
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  h2 {
    margin: 0;
    font-size: var(--font-size-xl);
    font-weight: 600;
    color: var(--color-text-primary);
  }
}

.add-button {
  transition: all var(--transition-normal);

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: var(--shadow-sm);
  }
}

.user-table {
  // 表格样式优化
  :deep(.ant-table-thead > tr > th) {
    background: var(--color-bg-tertiary);
    color: var(--color-text-primary);
    font-weight: 600;
    border-bottom: 1px solid var(--color-border);
  }

  :deep(.ant-table-tbody > tr > td) {
    border-bottom: 1px solid var(--color-border);
    transition: background var(--transition-normal);
  }

  :deep(.ant-table-tbody > tr:hover > td) {
    background: var(--color-bg-hover) !important;
  }
}

.status-tag {
  transition: all var(--transition-normal);
}

.action-button {
  transition: all var(--transition-normal);

  &:hover:not(:disabled) {
    opacity: 0.85;
    transform: translateY(-1px);
  }
}

// 弹窗样式
.user-modal {
  :deep(.ant-modal-content) {
    background: var(--color-card-bg);
    border: 1px solid var(--color-card-border);
    border-radius: 12px;
    box-shadow: var(--shadow-lg);
  }

  :deep(.ant-modal-header) {
    background: var(--color-card-bg);
    border-bottom: 1px solid var(--color-border);
  }

  :deep(.ant-modal-title) {
    color: var(--color-text-primary);
    font-weight: 600;
  }

  :deep(.ant-form-item-label > label) {
    color: var(--color-text-secondary);
  }

  :deep(.ant-input),
  :deep(.ant-input-affix-wrapper),
  :deep(.ant-select-selector) {
    background: var(--color-bg-secondary);
    border-color: var(--color-border);
    transition: all var(--transition-normal);

    &:hover {
      border-color: var(--color-primary);
    }

    &:focus {
      border-color: var(--color-primary);
      box-shadow: 0 0 0 2px rgba(19, 75, 234, 0.1);
    }
  }
}
</style>
