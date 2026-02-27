import sys

filepath = sys.argv[1]

with open(filepath, "r") as f:
    content = f.read()

# Add the emoji mapping and reaction functions before the feishuPlugin definition
reaction_code = r'''
// --- Patched: emoji reaction support ---
var UNICODE_TO_FEISHU_EMOJI = {
  "\ud83d\udc4d": "THUMBSUP", "\ud83d\udc4e": "ThumbsDown",
  "\ud83d\ude0a": "SMILE", "\ud83d\ude04": "LAUGH",
  "\ud83d\ude02": "LOL", "\ud83e\udd23": "LOL",
  "\u2764\ufe0f": "HEART", "\u2764": "HEART", "\ud83d\udc97": "HEART",
  "\ud83d\udd25": "Fire", "\ud83d\udc4f": "APPLAUSE",
  "\ud83d\ude4f": "THANKS", "\ud83d\udcaa": "MUSCLE",
  "\ud83c\udf89": "PARTY", "\ud83d\ude0d": "LOVE",
  "\ud83d\ude2d": "CRY", "\ud83d\ude22": "CRY",
  "\ud83d\ude2e": "SHOCKED", "\ud83d\ude31": "TERROR",
  "\ud83e\udd14": "THINKING", "\ud83d\ude09": "WINK",
  "\ud83d\ude33": "BLUSH", "\ud83d\ude24": "PROUD",
  "\ud83d\ude0f": "SMIRK", "\ud83e\udd26": "FACEPALM",
  "\u2705": "DONE", "\u2795": "JIAYI",
  "\ud83d\udc40": "GLANCE", "\ud83e\udef0": "FINGERHEART",
  "\ud83e\udd1c": "FISTBUMP", "\ud83d\ude21": "ANGRY",
  "\ud83d\udc3b": "BEAR", "\ud83c\udf7a": "BEER",
  "\u2615": "Coffee", "\ud83c\udf39": "ROSE",
  "\ud83c\udf81": "GIFT", "\ud83d\udcaf": "Hundred",
  "\u2b50": "Trophy", "\ud83e\udd1d": "SHAKE",
  "\ud83e\udd73": "Partying", "\ud83d\ude00": "JOYFUL",
  "\ud83c\udd97": "OK", "\ud83d\udc4c": "OK", "\ud83e\udee1": "SALUTE",
};

// Complete lowercase -> official emoji_type mapping (from Feishu API docs)
var NAME_TO_FEISHU_EMOJI = {
  "ok": "OK", "thumbsup": "THUMBSUP", "thanks": "THANKS",
  "muscle": "MUSCLE", "fingerheart": "FINGERHEART", "applause": "APPLAUSE",
  "fistbump": "FISTBUMP", "jiayi": "JIAYI", "plusone": "JIAYI", "done": "DONE",
  "smile": "SMILE", "blush": "BLUSH", "laugh": "LAUGH",
  "smirk": "SMIRK", "lol": "LOL", "facepalm": "FACEPALM",
  "love": "LOVE", "wink": "WINK", "proud": "PROUD",
  "witty": "WITTY", "smart": "SMART", "scowl": "SCOWL",
  "thinking": "THINKING", "sob": "SOB", "cry": "CRY",
  "error": "ERROR", "nosepick": "NOSEPICK", "haughty": "HAUGHTY",
  "slap": "SLAP", "spitblood": "SPITBLOOD", "toasted": "TOASTED",
  "glance": "GLANCE", "dull": "DULL", "innocentsmile": "INNOCENTSMILE",
  "joyful": "JOYFUL", "wow": "WOW", "trick": "TRICK",
  "yeah": "YEAH", "enough": "ENOUGH", "tears": "TEARS",
  "embarrassed": "EMBARRASSED", "kiss": "KISS", "smooch": "SMOOCH",
  "drool": "DROOL", "obsessed": "OBSESSED", "money": "MONEY",
  "tease": "TEASE", "showoff": "SHOWOFF", "comfort": "COMFORT",
  "clap": "CLAP", "praise": "PRAISE", "strive": "STRIVE",
  "xblush": "XBLUSH", "silent": "SILENT", "wave": "WAVE",
  "what": "WHAT", "frown": "FROWN", "shy": "SHY",
  "dizzy": "DIZZY", "lookdown": "LOOKDOWN", "chuckle": "CHUCKLE",
  "wail": "WAIL", "crazy": "CRAZY", "whimper": "WHIMPER",
  "hug": "HUG", "blubber": "BLUBBER", "wronged": "WRONGED",
  "husky": "HUSKY", "shhh": "SHHH", "smug": "SMUG",
  "angry": "ANGRY", "hammer": "HAMMER", "shocked": "SHOCKED",
  "terror": "TERROR", "petrified": "PETRIFIED", "skull": "SKULL",
  "sweat": "SWEAT", "speechless": "SPEECHLESS", "sleep": "SLEEP",
  "drowsy": "DROWSY", "yawn": "YAWN", "sick": "SICK",
  "puke": "PUKE", "betrayed": "BETRAYED", "headset": "HEADSET",
  "slight": "SLIGHT", "tongue": "TONGUE", "eyesclosed": "EYESCLOSED",
  "calf": "CALF", "bear": "BEAR", "bull": "BULL",
  "rainbowpuke": "RAINBOWPUKE", "rose": "ROSE", "heart": "HEART",
  "party": "PARTY", "lips": "LIPS", "beer": "BEER", "cake": "CAKE",
  "gift": "GIFT", "cucumber": "CUCUMBER", "bomb": "BOMB",
  "fireworks": "FIREWORKS", "redpacket": "REDPACKET", "fortune": "FORTUNE",
  "luck": "LUCK", "firecracker": "FIRECRACKER", "heartbroken": "HEARTBROKEN",
  "poop": "POOP", "awesomen": "AWESOMEN", "salute": "SALUTE",
  "shake": "SHAKE", "highfive": "HIGHFIVE", "upperleft": "UPPERLEFT",
  "cleaver": "CLEAVER", "candiedhaws": "CANDIEDHAWS",
  // Mixed-case official emoji_type values (case-sensitive in Feishu API!)
  "eatingfood": "EatingFood", "mememe": "MeMeMe", "sigh": "Sigh",
  "typing": "Typing", "lemon": "Lemon", "get": "Get",
  "lgtm": "LGTM", "onit": "OnIt", "onesecond": "OneSecond",
  "vrheadset": "VRHeadset", "youarethebest": "YouAreTheBest",
  "thumbsdown": "ThumbsDown", "roarforyou": "RoarForYou",
  "drumstick": "Drumstick", "pepper": "Pepper", "bubbletea": "BubbleTea",
  "coffee": "Coffee", "yes": "Yes", "no": "No",
  "okr": "OKR", "checkmark": "CheckMark", "crossmark": "CrossMark",
  "minusone": "MinusOne", "hundred": "Hundred",
  "pin": "Pin", "alarm": "Alarm", "loudspeaker": "Loudspeaker",
  "trophy": "Trophy", "fire": "Fire", "music": "Music",
  "xmastree": "XmasTree", "snowman": "Snowman", "xmashat": "XmasHat",
  "stickyriceballs": "StickyRiceBalls", "soccer": "Soccer",
  "basketball": "Basketball", "fullmoonface": "FullMoonFace",
  "partying": "Partying", "gogogo": "GoGoGo",
  "thanksface": "ThanksFace", "saluteface": "SaluteFace", "shrug": "Shrug",
  "clownface": "ClownFace", "happydragon": "HappyDragon",
  "beamingface": "BeamingFace", "delighted": "Delighted", "coldsweat": "ColdSweat",
  "statusflashofinspiration": "StatusFlashOfInspiration", "18x": "18X",
  "movie": "Movie", "tv": "TV", "pumpkin": "Pumpkin",
  "moonrabbit": "MoonRabbit", "mooncake": "Mooncake",
  "jubilantrabbit": "JubilantRabbit",
};

function resolveFeishuEmoji(emoji) {
  if (!emoji) return "OK";
  // 1. Try unicode lookup
  var stripped = emoji.replace(/\uFE0F/g, "").trim();
  var fromUnicode = UNICODE_TO_FEISHU_EMOJI[stripped] || UNICODE_TO_FEISHU_EMOJI[emoji];
  if (fromUnicode) return fromUnicode;
  // 2. Try name lookup (case-insensitive)
  var lower = emoji.toLowerCase().trim();
  var fromName = NAME_TO_FEISHU_EMOJI[lower];
  if (fromName) return fromName;
  // 3. Try exact match (maybe agent sent correct casing already)
  var values = Object.values(NAME_TO_FEISHU_EMOJI);
  if (values.indexOf(emoji) !== -1) return emoji;
  // 4. Fallback to OK instead of invalid type
  return "OK";
}

async function sendFeishuReaction(cfg, messageId, emoji) {
  var client = createFeishuClientFromConfig(cfg);
  var emojiType = resolveFeishuEmoji(emoji);
  var result = await client.im.v1.messageReaction.create({
    path: { message_id: messageId },
    data: { reaction_type: { emoji_type: emojiType } }
  });
  return {
    reactionId: result?.data?.reaction_id ?? "",
    emojiType: emojiType
  };
}

async function deleteFeishuReaction(cfg, messageId, reactionId) {
  var client = createFeishuClientFromConfig(cfg);
  await client.im.v1.messageReaction.delete({
    path: { message_id: messageId, reaction_id: reactionId }
  });
}

// --- Patched: document support ---
function markdownToFeishuBlocks(text) {
  var lines = text.split("\n");
  var blocks = [];
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    if (line.trim() === "") continue;
    if (line.trim() === "---" || line.trim() === "***") {
      blocks.push({ block_type: 22 }); // divider
      continue;
    }
    var headingMatch = line.match(/^(#{1,9})\s+(.+)/);
    if (headingMatch) {
      var level = headingMatch[1].length; // 1-9
      var blockType = 2 + level; // heading1=3, heading2=4, ...
      var hBlock = { block_type: blockType };
      var hKey = "heading" + level;
      hBlock[hKey] = { elements: [{ text_run: { content: headingMatch[2] } }] };
      blocks.push(hBlock);
      continue;
    }
    var bulletMatch = line.match(/^[-*]\s+(.+)/);
    if (bulletMatch) {
      blocks.push({
        block_type: 12,
        bullet: { elements: [{ text_run: { content: bulletMatch[1] } }] }
      });
      continue;
    }
    var orderedMatch = line.match(/^\d+\.\s+(.+)/);
    if (orderedMatch) {
      blocks.push({
        block_type: 13,
        ordered: { elements: [{ text_run: { content: orderedMatch[1] } }] }
      });
      continue;
    }
    var quoteMatch = line.match(/^>\s+(.+)/);
    if (quoteMatch) {
      blocks.push({
        block_type: 15,
        quote: { elements: [{ text_run: { content: quoteMatch[1] } }] }
      });
      continue;
    }
    // Default: text block
    blocks.push({
      block_type: 2,
      text: { elements: [{ text_run: { content: line } }] }
    });
  }
  return blocks;
}

async function createFeishuDocument(cfg, title, content, folderToken) {
  var client = createFeishuClientFromConfig(cfg);
  var createData = {};
  if (title) createData.title = title;
  if (folderToken) createData.folder_token = folderToken;
  var docResult = await client.docx.v1.document.create({ data: createData });
  var doc = docResult?.data?.document;
  if (!doc || !doc.document_id) {
    throw new Error("Failed to create Feishu document: " + JSON.stringify(docResult));
  }
  var documentId = doc.document_id;
  if (content && content.trim()) {
    var blocks = markdownToFeishuBlocks(content);
    if (blocks.length > 0) {
      await client.docx.v1.documentBlockChildren.create({
        path: { document_id: documentId, block_id: documentId },
        data: { children: blocks },
        params: { document_revision_id: -1 }
      });
    }
  }
  var docUrl = "https://feishu.cn/docx/" + documentId;
  return { documentId: documentId, title: title || "", url: docUrl };
}

async function appendFeishuDocument(cfg, documentId, content) {
  var client = createFeishuClientFromConfig(cfg);
  if (!content || !content.trim()) {
    throw new Error("content is required for appendDocument");
  }
  var blocks = markdownToFeishuBlocks(content);
  if (blocks.length === 0) {
    return { documentId: documentId, blocksAdded: 0 };
  }
  var result = await client.docx.v1.documentBlockChildren.create({
    path: { document_id: documentId, block_id: documentId },
    data: { children: blocks },
    params: { document_revision_id: -1 }
  });
  return {
    documentId: documentId,
    blocksAdded: blocks.length,
    children: result?.data?.children?.length ?? 0
  };
}
// --- Patched: sendAttachment support ---
async function uploadFeishuImage(cfg, filePath) {
  var client = createFeishuClientFromConfig(cfg);
  var fs = await import("node:fs");
  var path = await import("node:path");
  var stream = fs.createReadStream(filePath);
  var result = await client.im.v1.image.create({
    data: { image_type: "message", image: stream }
  });
  if (!result || !result.image_key) {
    throw new Error("Failed to upload image to Feishu: " + JSON.stringify(result));
  }
  return result.image_key;
}

async function sendFeishuImageMessage(cfg, to, imageKey, receiveIdType) {
  var client = createFeishuClientFromConfig(cfg);
  var content = JSON.stringify({ image_key: imageKey });
  var result = await client.im.v1.message.create({
    params: { receive_id_type: receiveIdType || "chat_id" },
    data: { receive_id: to, msg_type: "image", content: content }
  });
  return {
    messageId: result?.data?.message_id ?? "",
    chatId: to
  };
}

async function sendFeishuFileMessage(cfg, to, filePath, receiveIdType) {
  var client = createFeishuClientFromConfig(cfg);
  var fs = await import("node:fs");
  var path = await import("node:path");
  var ext = path.extname(filePath).toLowerCase();
  var imageExts = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".ico"];
  if (imageExts.indexOf(ext) !== -1) {
    var imageKey = await uploadFeishuImage(cfg, filePath);
    return await sendFeishuImageMessage(cfg, to, imageKey, receiveIdType);
  }
  // For non-image files, send as text link
  var fileName = path.basename(filePath);
  var textResult = await sendMessageFeishu({ cfg: cfg, to: to, text: "[File: " + fileName + "]", receiveIdType: receiveIdType });
  return textResult;
}
// --- End patched sendAttachment support ---
// --- End patched document support ---
// --- End patched reaction support ---

'''

# Insert reaction code before feishuPlugin definition
old_plugin_start = 'var feishuPlugin = {'
content = content.replace(old_plugin_start, reaction_code + old_plugin_start, 1)

# Add actions section before outbound in the plugin
old_outbound = '  outbound: feishuOutbound,'
new_actions_and_outbound = '''  actions: {
    listActions: ({ cfg }) => {
      if (!cfg.channels?.feishu) return [];
      return ["react", "createDocument", "appendDocument", "sendAttachment"];
    },
    supportsAction: ({ action }) => ["react", "createDocument", "appendDocument", "sendAttachment"].indexOf(action) !== -1,
    handleAction: async ({ action, params, cfg }) => {
      var feishuCfg = cfg.channels?.feishu;
      if (!feishuCfg) {
        throw new Error("Feishu channel not configured");
      }
      if (action === "react") {
        var messageId = params.messageId;
        if (!messageId || typeof messageId !== "string") {
          throw new Error("messageId is required for react action");
        }
        var emoji = params.emoji;
        var remove = params.remove;
        if (remove && params.reactionId) {
          await deleteFeishuReaction(feishuCfg, messageId, params.reactionId);
          var _r = { ok: true, removed: true }; return { content: [{ type: "text", text: JSON.stringify(_r) }], details: _r };
        }
        if (!emoji) {
          throw new Error("emoji is required for react action");
        }
        var result = await sendFeishuReaction(feishuCfg, messageId, emoji);
        var _r = { ok: true, reactionId: result.reactionId, emojiType: result.emojiType }; return { content: [{ type: "text", text: JSON.stringify(_r) }], details: _r };
      }
      if (action === "createDocument") {
        var title = params.title || params.message || "";
        var content = params.content || params.text || "";
        var folderToken = params.folderToken || params.folder || undefined;
        var result = await createFeishuDocument(feishuCfg, title, content, folderToken);
        var _r = { ok: true, documentId: result.documentId, title: result.title, url: result.url };
        return { content: [{ type: "text", text: JSON.stringify(_r) }], details: _r };
      }
      if (action === "appendDocument") {
        var documentId = params.documentId;
        if (!documentId || typeof documentId !== "string") {
          throw new Error("documentId is required for appendDocument action");
        }
        var content = params.content || params.text || params.message || "";
        var result = await appendFeishuDocument(feishuCfg, documentId, content);
        var _r = { ok: true, documentId: result.documentId, blocksAdded: result.blocksAdded };
        return { content: [{ type: "text", text: JSON.stringify(_r) }], details: _r };
      }
      if (action === "sendAttachment") {
        var to = params.to || params.target;
        if (!to || typeof to !== "string") {
          throw new Error("to/target is required for sendAttachment");
        }
        var filePath = params.path || params.filePath || params.media;
        if (!filePath) {
          throw new Error("path/filePath/media is required for sendAttachment");
        }
        var { targetId, receiveIdType } = parseTarget(to);
        var result = await sendFeishuFileMessage(feishuCfg, targetId, filePath, receiveIdType);
        var _r = { ok: true, messageId: result.messageId, chatId: result.chatId };
        return { content: [{ type: "text", text: JSON.stringify(_r) }], details: _r };
      }
      throw new Error("Action " + action + " is not supported for feishu.");
    },
  },
  outbound: feishuOutbound,'''

content = content.replace(old_outbound, new_actions_and_outbound, 1)

# Enable reactions capability
content = content.replace('reactions: false', 'reactions: true', 1)

# Add sendMedia to feishuOutbound (required by core outbound delivery)
old_outbound_end = '''    return {
      channel: "feishu",
      messageId: result.messageId,
      chatId: result.chatId,
      conversationId: result.chatId
    };
  }
};'''

new_outbound_end = '''    return {
      channel: "feishu",
      messageId: result.messageId,
      chatId: result.chatId,
      conversationId: result.chatId
    };
  },
  sendMedia: async (params) => {
    const { cfg, to, text, mediaUrl } = params;
    const feishuCfg = cfg.channels?.feishu;
    if (!feishuCfg) {
      throw new Error("Feishu channel not configured");
    }
    const { targetId, receiveIdType } = parseTarget(to);
    // Send caption text with media URL link
    var mediaText = text || "";
    if (mediaUrl) {
      mediaText = mediaText ? mediaText + "\\n" + mediaUrl : mediaUrl;
    }
    if (!mediaText) mediaText = "(media)";
    const result = await sendMessageFeishu({
      cfg: feishuCfg,
      to: targetId,
      text: mediaText,
      receiveIdType
    });
    return {
      channel: "feishu",
      messageId: result.messageId,
      chatId: result.chatId,
      conversationId: result.chatId
    };
  }
};'''

content = content.replace(old_outbound_end, new_outbound_end, 1)

# Add messaging.targetResolver so feishu IDs (oc_/ou_/om_) are recognized as targets
old_capabilities_end = '''    polls: false
  },
  configSchema:'''

new_capabilities_end = '''    polls: false
  },
  messaging: {
    targetResolver: {
      looksLikeId: () => true,
      hint: "Feishu chat_id (oc_xxx), user_id (ou_xxx), or message_id (om_xxx)",
    },
  },
  configSchema:'''

content = content.replace(old_capabilities_end, new_capabilities_end, 1)

with open(filepath, "w") as f:
    f.write(content)

print("Feishu reaction patch applied successfully (reactions + targetResolver + full emoji mapping)")
