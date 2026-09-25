import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We have:
# 309:               </div>
# 310:             </div>
# 311:             </div>
# 312:           </div>
# 313:         </div>
# 314: 
# 315:         <!-- TABLES SECTION -->
# We need to remove one extra </div>.
# But wait, let's trace EXACTLY.
# <div class="flex-1 flex flex-col gap-6 overflow-y-auto pr-2 pb-10" id="main-left-column">
#   <!-- METRICS -->
#   <div class="grid grid-cols-4 gap-4"> ... </div>
#   <!-- CHARTS SECTION -->
#   <div class="grid grid-cols-5 gap-4">
#       <div class="col-span-3">...</div>
#       <div class="col-span-2">
#           <div class="flex-1 flex items-center justify-between">
#               <div donut></div>
#               <div legend></div>
#           </div>
#       </div>
#   </div>

# So from the legend end (which is </div> at line 309):
# 310: </div> (closes legend parent flex-1 justify-between)
# 311: </div> (closes col-span-2)
# 312: </div> (closes grid-cols-5)
# 313: </div> (closes main-left-column) -> THIS IS THE BUG!
# We must REMOVE line 313!

# Let's replace the block:
block_to_replace = """              </div>
            </div>
            </div>
          </div>
        </div>

        <!-- TABLES SECTION -->"""

correct_block = """              </div>
            </div>
          </div>
        </div>

        <!-- TABLES SECTION -->"""

content = content.replace(block_to_replace, correct_block)

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Extra div removed.")
