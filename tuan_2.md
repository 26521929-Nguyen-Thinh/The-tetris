# Tuần 2 - Phân chia công việc code game Tetris

Toàn bộ code nằm trong 1 file `main.py`. Mỗi người code trên **branch riêng**, tạo Pull Request vào `main`. Nhóm trưởng review và merge.

## Cách code song song trong 1 file

Conflict chỉ xảy ra khi 2 người sửa cùng chỗ trong file. Vì vậy:

1. `main.py` đã có sẵn **khung**: mọi biến, mọi hàm (thân hàm tạm thời rỗng, trả giá trị mặc định) và vòng lặp `main()` đã gọi sẵn các hàm. Game vẫn chạy được như cũ. Hàm của mỗi người nằm trong vùng có comment `# ===== Tên: ... =====`.
2. Mọi người tạo branch từ `main` mới nhất, **chỉ viết thân các hàm trong vùng của mình**. Không sửa `main()`, không sửa hàm của người khác. Các vùng nằm ở các vị trí khác nhau nên merge theo thứ tự nào cũng không conflict.
3. Muốn thêm hàm phụ thì đặt ngay dưới hàm của mình, đặt tên có tiền tố riêng (ví dụ `lam_...`).

## Bảng phân công

| STT | Thành viên | Branch | Phần phụ trách | Hàm phụ trách |
| --- | ---------- | ------ | -------------- | ------------- |
| 1 | Nguyễn Thịnh (nhóm trưởng) | `main` | Review, test, merge PR | - |
| 2 | Nguyễn Việt Lâm | `feat/control` | Khối, điều khiển, xoay | `blocks`, `canMove`, `block2Board`, `boardDelBlock`, `rotate`, `newBlock`, `handleKey` |
| 3 | Trương Tấn Phát | `feat/line` | Xóa dòng, level, tốc độ | `removeLine`, `getLevel`, `getSpeed` |
| 4 | Thái Trí Nhân | `feat/score` | Điểm, game over, chơi lại | `addScore`, `isGameOver`, `gameOverScreen`, `resetGame` |
| 5 | Võ Ngọc Thơ | `feat/ui` | Giao diện | `draw` |

## Quy ước dữ liệu chung

- `board`: `H = 20` dòng, `W = 15` cột, mỗi ô 1 ký tự. `'#'` là viền, `' '` là ô trống, chữ cái (`'I'`, `'T'`...) là ô có khối. Vùng chơi: dòng `1` đến `H - 2`, cột `1` đến `W - 2`.
- `cur`: ma trận 4x4 của khối đang rơi. `x`, `y`: vị trí góc trên trái của `cur` trên `board`.
- `nextB`: số thứ tự khối tiếp theo trong `blocks`.
- `score`, `level`, `lines`, `speed`: điểm, cấp độ, tổng số dòng đã xóa, số giây chờ mỗi lần khối rơi.

## Chi tiết từng phần

### Lâm - khối, điều khiển, xoay

| Hàm | Việc cần làm |
| --- | ------------ |
| `blocks` | Còn đúng 7 khối: I, O, T, S, Z, J, L. Hiện tại list có 16 phần tử nhưng chỉ random 7 phần tử đầu (toàn I và O). Dòng đầu của mỗi ma trận để trống, vì khối sinh ở `y = 0` sẽ đè viền trên. |
| `canMove`, `block2Board`, `boardDelBlock` | Đổi `blocks[b]` thành `cur`, để xoay không làm hỏng list `blocks`. |
| `rotate(m)` | Trả về ma trận 4x4 mới, là `m` xoay 90 độ theo chiều kim đồng hồ. Không sửa `m`. |
| `newBlock()` | `cur` = copy của `blocks[nextB]`, random `nextB` mới (0 đến 6), `x = 5`, `y = 0`. |
| `handleKey(c)` | `a` sang trái, `d` sang phải, `s` xuống 1 ô, `w` xoay (nếu xoay xong bị đè thì trả lại hình cũ), `space` thả thẳng xuống đáy, `p` tạm dừng đến khi bấm `p` lần nữa. Bấm `q` thì trả về `'quit'`, các phím khác trả về `None`. Chỉ di chuyển khi `canMove(...)` cho phép. |

Tự test: chơi thử, đủ 7 khối, xoay sát viền trái, phải và sát khối khác không bị lỗi.

### Phát - xóa dòng, level, tốc độ

| Hàm | Việc cần làm |
| --- | ------------ |
| `removeLine()` | Tìm dòng đầy (mọi ô từ cột `1` đến `W - 2` khác `' '`). Xóa dòng đó, dời các dòng phía trên xuống 1 dòng, dòng `1` thành dòng trống có viền `'#'` 2 bên. Trả về số dòng đã xóa (0 đến 4). Lưu ý: sau khi dời phải kiểm tra lại chính dòng đó, vì dòng mới dời xuống cũng có thể đầy. |
| `getLevel(totalLines)` | Trả về `totalLines // 10 + 1` (mỗi 10 dòng lên 1 level, theo docs). |
| `getSpeed(level)` | Level 1 trả về `0.5`, mỗi level giảm `0.05`, thấp nhất `0.1`. |

Tự test: tạm sửa `initBoard()` trên máy mình cho sẵn 2 dòng gần đầy, chơi để lấp đầy, xem 2 dòng biến mất và các dòng trên rơi xuống đúng. Không commit phần sửa tạm này.

### Nhân - điểm, game over, chơi lại

| Hàm | Việc cần làm |
| --- | ------------ |
| `addScore(score, n, level)` | Trả về điểm mới. Xóa 1/2/3/4 dòng được 100/300/500/800 điểm, nhân với `level` (theo docs). `n = 0` thì không cộng. |
| `isGameOver()` | Trả `True` nếu khối vừa sinh ra không còn chỗ (dùng `canMove(0, 0)`). |
| `gameOverScreen()` | Xóa màn hình, in "GAME OVER", điểm của ván, điểm cao nhất (đọc và ghi file `highscore.txt`, file chưa có thì coi là 0). Chờ người chơi bấm `r` hoặc `q`, trả về `'r'` hoặc `'q'`. |
| `resetGame()` | Đưa về ván mới: `initBoard()`, `score = 0`, `lines = 0`, `level = 1`, `speed = 0.5`, gọi `newBlock()`. |

Tự test: chơi đến khi chồng khối chạm đỉnh, kiểm tra hiện màn hình game over, bấm `r` chơi lại được, bấm `q` thoát được, điểm cao được lưu.

### Thơ - giao diện

| Hàm | Việc cần làm |
| --- | ------------ |
| `draw()` | Xóa màn hình rồi vẽ `board`: ô `'#'` in `'▓▓'`, ô có khối in `'██'`, ô trống in `'  '` (2 space, để ô vuông không bị dẹt). Bên phải board, ở 3 dòng đầu, in `Score: ...`, `Level: ...`, `Lines: ...` (đọc từ biến `score`, `level`, `lines`). |

Gợi ý: ghép mỗi dòng thành 1 chuỗi rồi mới `print`, game sẽ đỡ giật hơn in từng ký tự.

Làm thêm nếu còn thời gian (không bắt buộc):
- Thay `os.system("cls")` bằng `print("\033[H", end="")` để hết nhấp nháy.
- In khối tiếp theo (`blocks[nextB]`) dưới dòng `Lines`.

## Quy định

- Mỗi người chỉ sửa thân các hàm thuộc phần mình. Muốn sửa phần của người khác thì báo trước.
- Không sửa `main()`. Cần đổi thì báo nhóm trưởng.
- Code phải chạy được `python main.py` mà không lỗi trước khi gửi review.
- Commit message ghi rõ thay đổi, ví dụ `[Feat] Thêm removeLine`.
- Cập nhật thẻ Trello khi bắt đầu và khi xong.
