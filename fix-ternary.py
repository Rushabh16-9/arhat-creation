with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

# We need to replace the last `)}` before `</main>` with `) : null}`
old_tail = '''              </tbody>
            </table>
          </div>
        )}
      </main>'''

new_tail = '''              </tbody>
            </table>
          </div>
        ) : null}
      </main>'''

js = js.replace(old_tail, new_tail)

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Ternary fixed!")
