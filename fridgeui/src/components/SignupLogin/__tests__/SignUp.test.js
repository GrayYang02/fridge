/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import SignUp from '../SignUp';
import api from '../../../api';

// 为了捕获路由变化，我们创建一个辅助组件，用于显示当前路径
function LocationDisplay() {
  const location = useLocation();
  return <div data-testid="location-display">{location.pathname}</div>;
}

const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => {
  const originalModule = jest.requireActual('react-router-dom');
  return {
    ...originalModule,
    useNavigate: () => mockNavigate,
  };
});
// 对 api.post 进行 mock
jest.mock('../../../api', () => ({
  post: jest.fn()
}));

// 每个测试前清理 mock 并重置全局 alert
beforeEach(() => {
  jest.clearAllMocks();
  global.alert = jest.fn();
});

// 辅助函数：将组件包裹在 MemoryRouter 中，配置初始路由和路由规则
function renderWithRouter(ui, { route = '/signup' } = {}) {
  return render(
    <MemoryRouter initialEntries={[route]}>
      <Routes>
        <Route path="/signup" element={ui} />
        <Route path="/login" element={<LocationDisplay />} />
      </Routes>
    </MemoryRouter>
  );
}

describe('SignUp 组件测试', () => {
  test('渲染测试：组件应正确显示各输入框及按钮', () => {
    renderWithRouter(<SignUp />);
    // 由于组件中使用 label 标签展示文本，可以通过 getByText 检查
    expect(screen.getByText(/EMAIL/i)).toBeInTheDocument();
    expect(screen.getByText(/PASSWORD/i)).toBeInTheDocument();
    expect(screen.getByText(/USERNAME/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument();
  });

  test('成功注册测试：提交表单后应显示成功提示并导航到 /login', async () => {
    // 模拟 API 请求成功
    api.post.mockResolvedValueOnce({ data: { message: 'ok' } });

    renderWithRouter(<SignUp />);

    // 通过 label 文本查找输入框，注意：如果 label 与 input 没有关联，则需修改组件（建议为 input 添加 placeholder 或 htmlFor 属性）
    const emailInput = screen.getByLabelText(/EMAIL/i);
    const usernameInput = screen.getByLabelText(/USERNAME/i);
    const passwordInput = screen.getByLabelText(/PASSWORD/i);

    // 模拟用户输入
    await userEvent.type(emailInput, 'test@example.com');
    await userEvent.type(usernameInput, 'testuser');
    await userEvent.type(passwordInput, 'password123');

    // 提交表单
    await userEvent.click(screen.getByRole('button', { name: /sign up/i }));

    // 等待异步操作完成，断言调用成功提示和页面跳转
    await waitFor(() => {
      expect(global.alert).toHaveBeenCalledWith('Sign Up Successful!');
    });
    // 验证当前路由为 /login
    await waitFor(() => {
      expect(screen.getByTestId('location-display')).toHaveTextContent('/login');
    });
  });

  test('失败注册测试：提交表单后应显示失败提示', async () => {
    // 模拟 API 请求失败
    api.post.mockRejectedValueOnce(new Error('Network Error'));

    renderWithRouter(<SignUp />);

    const emailInput = screen.getByLabelText(/EMAIL/i);
    const usernameInput = screen.getByLabelText(/USERNAME/i);
    const passwordInput = screen.getByLabelText(/PASSWORD/i);

    await userEvent.type(emailInput, 'test@example.com');
    await userEvent.type(usernameInput, 'testuser');
    await userEvent.type(passwordInput, 'password123');

    await userEvent.click(screen.getByRole('button', { name: /sign up/i }));

    await waitFor(() => {
      expect(global.alert).toHaveBeenCalledWith('Sign Up Failed!');
    });
  });
});
